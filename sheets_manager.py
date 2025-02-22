from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import logging
import json
import os

class SheetsManager:
    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def get_service(self):
        """Initialize Google Sheets service"""
        try:
            # Get credentials from environment variable
            creds_json = os.environ.get('GOOGLE_SHEETS_CREDENTIALS')
            if not creds_json:
                raise ValueError("Google Sheets credentials not found in environment")

            try:
                # Remove any whitespace and ensure we have a clean JSON string
                creds_json = creds_json.strip()

                # Parse credentials JSON
                creds_dict = json.loads(creds_json)

                # Log credential structure (without sensitive data)
                self.logger.info("Credential keys found: " + ", ".join(creds_dict.keys()))

                # Create credentials object using the correct method
                creds = Credentials.from_service_account_info(
                    creds_dict,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )

                service = build('sheets', 'v4', credentials=creds)
                self.logger.info("Successfully created Sheets service")
                return service

            except json.JSONDecodeError as je:
                self.logger.error(f"Invalid JSON format in credentials: {str(je)}")
                raise ValueError(f"Invalid JSON format in Google Sheets credentials: {str(je)}")

        except Exception as e:
            self.logger.error(f"Error initializing Sheets service: {str(e)}")
            raise

    def update_sheet(self, df):
        """Update Google Sheet with new reviews"""
        try:
            service = self.get_service()

            # Convert DataFrame to values
            values = [df.columns.values.tolist()] + df.values.tolist()

            body = {
                'values': values
            }

            # Clear existing data
            service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id,
                range='Sheet1'
            ).execute()

            # Update with new data
            result = service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='Sheet1',
                valueInputOption='RAW',
                body=body
            ).execute()

            self.logger.info(f"Updated {result.get('updatedCells')} cells")
            return True

        except HttpError as e:
            self.logger.error(f"Google Sheets API error: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error updating sheet: {str(e)}")
            raise