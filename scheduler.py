import schedule
import time
from datetime import datetime
import logging
from review_scraper import PlayStoreReviewer
from sheets_manager import SheetsManager
from config import SCHEDULE_TIME

class ReviewScheduler:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.last_run = None
        self.last_status = None
        self.error_message = None
        self.package_name = None
        self.spreadsheet_id = None

    def update_config(self, package_name, spreadsheet_id):
        """Update configuration settings"""
        self.package_name = package_name
        self.spreadsheet_id = spreadsheet_id
        self.logger.info(f"Configuration updated - Package: {package_name}, Sheet ID: {spreadsheet_id}")

    def job(self):
        """Execute the review scraping and updating task"""
        try:
            if not self.package_name or not self.spreadsheet_id:
                raise ValueError("Package name and Google Sheet ID must be configured before running the job")

            self.logger.info("Starting scheduled job")
            self.last_status = "Running"
            self.error_message = None

            # Initialize components
            reviewer = PlayStoreReviewer(self.package_name)
            sheets_mgr = SheetsManager(self.spreadsheet_id)

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
            raise

    def start(self):
        """Start the scheduler"""
        schedule.every().day.at(SCHEDULE_TIME).do(self.job)

        while True:
            schedule.run_pending()
            time.sleep(60)