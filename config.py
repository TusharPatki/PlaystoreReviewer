# Configuration settings
PACKAGE_NAME = "com.yaper.android"  # Yaper app package name
SPREADSHEET_ID = None  # Will be set from environment variable for security
SCHEDULE_TIME = "00:00"  # Daily execution time (midnight)

# Load configuration from environment
import os

def clean_spreadsheet_id(sheet_id):
    """Clean the spreadsheet ID by removing any URL components"""
    if not sheet_id:
        return None
    # Remove 'd/' prefix if present
    if 'd/' in sheet_id:
        sheet_id = sheet_id.split('d/')[-1]
    # Remove any trailing parts
    sheet_id = sheet_id.split('/')[0]
    return sheet_id

SPREADSHEET_ID = clean_spreadsheet_id(os.environ.get('GOOGLE_SHEETS_ID'))