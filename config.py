# Configuration settings
PACKAGE_NAME = "your.app.package.name"  # Replace with your app's package name
SPREADSHEET_ID = None  # Will be set from environment variable for security
SCHEDULE_TIME = "00:00"  # Daily execution time (midnight)

# Load configuration from environment
import os
SPREADSHEET_ID = os.environ.get('GOOGLE_SHEETS_ID', SPREADSHEET_ID)