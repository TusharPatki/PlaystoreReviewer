# Play Store Review Scraper Dashboard

A real-time Google Play Store review monitoring dashboard that automatically fetches and analyzes app reviews, storing them in Google Sheets and providing instant notifications through Slack.

## Features

- 🔄 Automated review scraping from Google Play Store
- 📊 Interactive Streamlit dashboard for data visualization
- 📝 Google Sheets integration for data storage
- 🔔 Slack notifications for new reviews
- ⏰ Scheduled daily updates
- 🔍 Preview of latest reviews

## Setup

### Prerequisites

- Python 3.11
- Google Cloud Project with Sheets API enabled
- Slack Webhook URL (for notifications)
- Google Sheets Service Account Credentials

### Environment Variables

The following environment variables are required:

- `GOOGLE_SHEETS_ID`: The ID of your Google Sheet
- `GOOGLE_SHEETS_CREDENTIALS`: Service account credentials JSON
- `SLACK_WEBHOOK_URL`: Webhook URL for Slack notifications

### Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd play-store-review-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables

4. Run the application:
```bash
streamlit run app.py
```

## Usage

The dashboard provides:
- System status monitoring
- Manual trigger for review updates
- Latest reviews preview
- Configuration status

The scraper automatically runs daily at midnight (configurable in `config.py`).

## Development

The project structure:
```
├── app.py                 # Main Streamlit dashboard
├── config.py             # Configuration settings
├── review_scraper.py    # Play Store review scraping logic
├── scheduler.py         # Scheduled job management
└── sheets_manager.py    # Google Sheets integration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
