from google.oauth2.credentials import Credentials
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
                # Parse credentials JSON with strict parsing
                creds_dict = json.loads(creds_json.strip(), strict=True)

                # Validate required fields
                required_fields = ['client_email', 'private_key', 'project_id']
                missing_fields = [field for field in required_fields if field not in creds_dict]
                if missing_fields:
                    raise ValueError(f"Missing required fields in credentials: {', '.join(missing_fields)}")

                # Create credentials object
                creds = Credentials.from_service_account_info(
                    creds_dict,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )

                service = build('sheets', 'v4', credentials=creds)
                return service

            except json.JSONDecodeError as je:
                self.logger.error(f"Invalid JSON format in credentials: {str(je)}")
                raise ValueError("Invalid JSON format in Google Sheets credentials. Please check the format.")

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