from google_play_scraper import Sort, reviews
import pandas as pd
from datetime import datetime
import logging

class PlayStoreReviewer:
    def __init__(self, package_name):
        self.package_name = package_name
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def fetch_reviews(self, count=None):
        """Fetch all reviews from Google Play Store"""
        try:
            self.logger.info(f"Fetching reviews for package: {self.package_name}")
            all_reviews = []
            continuation_token = None
            batch_size = 100  # Fetch in batches of 100

            while True:
                result, continuation_token = reviews(
                    self.package_name,
                    lang='en',
                    country='us',
                    sort=Sort.NEWEST,
                    count=batch_size,
                    continuation_token=continuation_token
                )

                if not result:
                    break

                all_reviews.extend(result)
                self.logger.info(f"Fetched {len(result)} reviews. Total so far: {len(all_reviews)}")

                # If we have a count limit or no more reviews
                if count and len(all_reviews) >= count:
                    all_reviews = all_reviews[:count]
                    break

                if not continuation_token:
                    break

            if not all_reviews:
                self.logger.warning(f"No reviews found for package: {self.package_name}")
                return pd.DataFrame()

            # Convert to DataFrame
            df = pd.DataFrame(all_reviews)

            # Add timestamp
            df['scrape_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Select and rename columns, including userName
            df = df[[
                'reviewId', 'userName', 'content', 'score', 'thumbsUpCount',
                'reviewCreatedVersion', 'at', 'repliedAt',
                'scrape_timestamp'
            ]]

            self.logger.info(f"Successfully fetched total of {len(df)} reviews")
            return df

        except Exception as e:
            self.logger.error(f"Error fetching reviews: {str(e)}")
            raise