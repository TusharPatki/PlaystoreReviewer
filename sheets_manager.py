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

                # Check if these are web OAuth credentials
                if 'web' in creds_dict:
                    raise ValueError(
                        "OAuth 2.0 client credentials provided instead of service account credentials. "
                        "Please provide a service account JSON key that starts with {\"type\": \"service_account\"}"
                    )

                # Validate required fields for service account
                required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 
                                 'client_email', 'client_id', 'auth_uri', 'token_uri']
                missing_fields = [field for field in required_fields if field not in creds_dict]

                if missing_fields:
                    self.logger.error(f"Missing required fields in credentials: {', '.join(missing_fields)}")
                    raise ValueError(f"Service account info was not in the expected format, missing fields: {', '.join(missing_fields)}")

                # Verify this is a service account
                if creds_dict.get('type') != 'service_account':
                    raise ValueError("Invalid credentials type. Expected 'service_account'")

                # Log credential structure (without sensitive data)
                self.logger.info(f"Found credentials for service account: {creds_dict.get('client_email', 'unknown')}")

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
            # Try to read spreadsheet metadata
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

            # Verify permissions first
            self.check_permissions(service)

            # Convert DataFrame to values
            # Convert timestamps to strings before sending to Google Sheets
            df = df.copy()
            for col in df.columns:
                if df[col].dtype == 'datetime64[ns]':
                    df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
                elif hasattr(df[col].dtype, 'name') and df[col].dtype.name == 'Timestamp':
                    df[col] = df[col].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else '')

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