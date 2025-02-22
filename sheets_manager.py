from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import logging

class SheetsManager:
    def __init__(self, spreadsheet_id, credentials_file):
        self.spreadsheet_id = spreadsheet_id
        self.credentials_file = credentials_file
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def get_service(self):
        """Initialize Google Sheets service"""
        try:
            creds = Credentials.from_authorized_user_file(
                self.credentials_file, 
                ['https://www.googleapis.com/auth/spreadsheets']
            )
            service = build('sheets', 'v4', credentials=creds)
            return service
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
