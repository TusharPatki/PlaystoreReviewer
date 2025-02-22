import streamlit as st
import pandas as pd
from datetime import datetime
from scheduler import ReviewScheduler
from review_scraper import PlayStoreReviewer
from sheets_manager import SheetsManager
from config import clean_spreadsheet_id

def main():
    st.set_page_config(
        page_title="Play Store Review Scraper",
        page_icon="📱",
        layout="wide"
    )

    st.title("📱 Play Store Review Scraper Dashboard")

    # Initialize session state
    if 'scheduler' not in st.session_state:
        st.session_state.scheduler = ReviewScheduler()
    if 'package_name' not in st.session_state:
        st.session_state.package_name = "com.yaper.android"
    if 'spreadsheet_id' not in st.session_state:
        st.session_state.spreadsheet_id = None

    # Configuration Section
    st.header("Configuration")
    with st.form("config_form"):
        # App Package ID input
        new_package_name = st.text_input(
            "App Package ID",
            value=st.session_state.package_name,
            help="Example: com.example.app (Find this in your app's Play Store URL)"
        )

        # Google Sheet link input
        sheet_link = st.text_input(
            "Google Sheet Link",
            value="" if not st.session_state.spreadsheet_id else f"https://docs.google.com/spreadsheets/d/{st.session_state.spreadsheet_id}",
            help="Paste your Google Sheet URL here"
        )

        submit = st.form_submit_button("Update Configuration")

        if submit:
            st.session_state.package_name = new_package_name
            st.session_state.spreadsheet_id = clean_spreadsheet_id(sheet_link)
            st.success("Configuration updated successfully!")

    # Status Section
    st.header("System Status")
    col1, col2, col3 = st.columns(3)

    with col1:
        last_run = st.session_state.scheduler.last_run
        st.metric(
            "Last Run",
            last_run.strftime('%Y-%m-%d %H:%M:%S') if last_run else "Never"
        )

    with col2:
        status = st.session_state.scheduler.last_status or "Not Run"
        st.metric("Status", status)

    with col3:
        if st.button("Run Now"):
            try:
                with st.spinner("Fetching all reviews (this may take a while)..."):
                    # Update scheduler with current configuration
                    st.session_state.scheduler.update_config(
                        st.session_state.package_name,
                        st.session_state.spreadsheet_id
                    )
                    # Run the job
                    st.session_state.scheduler.job()
                    st.success("Job completed!")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Error Display
    if st.session_state.scheduler.error_message:
        st.error(f"Last Error: {st.session_state.scheduler.error_message}")

    # Preview Section
    st.header("Latest Reviews Preview")
    try:
        reviewer = PlayStoreReviewer(st.session_state.package_name)
        # Only fetch 5 reviews for preview
        df = reviewer.fetch_reviews(count=5)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No reviews available")
    except Exception as e:
        st.error(f"Error fetching preview: {str(e)}")

if __name__ == "__main__":
    main()