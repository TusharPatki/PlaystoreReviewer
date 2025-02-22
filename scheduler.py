import schedule
import time
from datetime import datetime
import logging
from review_scraper import PlayStoreReviewer
from sheets_manager import SheetsManager
from config import PACKAGE_NAME, SPREADSHEET_ID, SCHEDULE_TIME

class ReviewScheduler:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.last_run = None
        self.last_status = None
        self.error_message = None

    def job(self):
        """Execute the review scraping and updating task"""
        try:
            self.logger.info("Starting scheduled job")

            # Initialize components
            reviewer = PlayStoreReviewer(PACKAGE_NAME)
            sheets_mgr = SheetsManager(SPREADSHEET_ID)

            # Fetch reviews
            df = reviewer.fetch_reviews()

            # Update sheet
            sheets_mgr.update_sheet(df)

            self.last_run = datetime.now()
            self.last_status = "Success"
            self.error_message = None

            self.logger.info("Job completed successfully")

        except Exception as e:
            self.last_status = "Failed"
            self.error_message = str(e)
            self.logger.error(f"Job failed: {str(e)}")

    def start(self):
        """Start the scheduler"""
        schedule.every().day.at(SCHEDULE_TIME).do(self.job)

        while True:
            schedule.run_pending()
            time.sleep(60)