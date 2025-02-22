from google_play_scraper import Sort, reviews
import pandas as pd
from datetime import datetime
import logging

class PlayStoreReviewer:
    def __init__(self, package_name):
        self.package_name = package_name
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def fetch_reviews(self, count=100):
        """Fetch reviews from Google Play Store"""
        try:
            self.logger.info(f"Fetching {count} reviews for package: {self.package_name}")

            result, continuation_token = reviews(
                self.package_name,
                lang='en',
                country='us',
                sort=Sort.NEWEST,
                count=count
            )

            if not result:
                self.logger.warning(f"No reviews found for package: {self.package_name}")
                return pd.DataFrame()

            # Convert to DataFrame
            df = pd.DataFrame(result)

            # Add timestamp
            df['scrape_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Select and rename columns
            df = df[[
                'reviewId', 'content', 'score', 'thumbsUpCount',
                'reviewCreatedVersion', 'at', 'repliedAt',
                'scrape_timestamp'
            ]]

            self.logger.info(f"Successfully fetched {len(df)} reviews")
            return df

        except Exception as e:
            self.logger.error(f"Error fetching reviews: {str(e)}")
            raise