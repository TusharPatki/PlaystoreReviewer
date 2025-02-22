import streamlit as st
import pandas as pd
from datetime import datetime
from scheduler import ReviewScheduler
from review_scraper import PlayStoreReviewer
from sheets_manager import SheetsManager
from config import PACKAGE_NAME, SPREADSHEET_ID

def main():
    st.set_page_config(
        page_title="Play Store Review Scraper",
        page_icon="📱",
        layout="wide"
    )

    st.title("📱 Play Store Review Scraper Dashboard")

    # Initialize scheduler
    if 'scheduler' not in st.session_state:
        st.session_state.scheduler = ReviewScheduler()

    # Status Section
    st.header("System Status")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Last Run",
            st.session_state.scheduler.last_run.strftime('%Y-%m-%d %H:%M:%S') 
            if st.session_state.scheduler.last_run else "Never"
        )

    with col2:
        status = st.session_state.scheduler.last_status or "Not Run"
        st.metric("Status", status)

    with col3:
        if st.button("Run Now"):
            with st.spinner("Fetching all reviews (this may take a while)..."):
                st.session_state.scheduler.job()
                st.success("Job completed!")

    # Error Display
    if st.session_state.scheduler.error_message:
        st.error(f"Last Error: {st.session_state.scheduler.error_message}")

    # Preview Section
    st.header("Latest Reviews Preview")
    try:
        reviewer = PlayStoreReviewer(PACKAGE_NAME)
        # Only fetch 5 reviews for preview
        df = reviewer.fetch_reviews(count=5)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No reviews available")
    except Exception as e:
        st.error(f"Error fetching preview: {str(e)}")

    # Configuration Info
    st.header("Configuration")
    st.code(f"""
    Package Name: {PACKAGE_NAME}
    Google Sheet ID: {SPREADSHEET_ID}
    """)

if __name__ == "__main__":
    main()