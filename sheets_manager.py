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
                # Parse credentials JSON
                creds_dict = json.loads(creds_json)

                # Create credentials object
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

    def check_permissions(self, service):
        """Verify permissions on the spreadsheet"""
        try:
            service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
            self.logger.info("Successfully verified spreadsheet permissions")
            return True
        except HttpError as e:
            if e.resp.status == 403:
                service_account = e._get_reason().split(":")[-1].strip()
                raise ValueError(
                    f"Permission denied. Please share the Google Sheet with the service account email: {service_account} "
                    "and grant it 'Editor' access."
                )
            elif e.resp.status == 404:
                raise ValueError(
                    f"Spreadsheet not found. Please verify the spreadsheet ID: {self.spreadsheet_id}"
                )
            raise

    def update_sheet(self, df):
        """Update Google Sheet with new reviews"""
        try:
            service = self.get_service()
            self.check_permissions(service)

            # Make a copy to avoid modifying the original dataframe
            df = df.copy()

            # Convert all datetime columns to strings in ISO format
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(df[col].iloc[0], pd.Timestamp):
                    df[col] = df[col].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else '')

            # Replace NaN values with empty strings
            df = df.fillna('')

            # Convert DataFrame to values
            values = [df.columns.values.tolist()] + df.values.tolist()

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
                body={'values': values}
            ).execute()

            self.logger.info(f"Updated {result.get('updatedCells')} cells")
            return True

        except HttpError as e:
            self.logger.error(f"Google Sheets API error: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error updating sheet: {str(e)}")
            raise