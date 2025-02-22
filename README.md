# Play Store Review Scraper Dashboard 📱

A real-time Google Play Store review monitoring dashboard that automatically fetches and analyzes app reviews, storing them in Google Sheets and providing instant notifications through Slack.

![Dashboard Preview](generated-icon.png)

## 🌟 Features

- **Automated Review Scraping** - Continuously monitors and fetches reviews from Google Play Store
- **Unlimited Review History** - Captures all available reviews without limitation
- **Interactive Dashboard** - Real-time Streamlit interface for data visualization
- **Google Sheets Integration** - Automatic data storage and synchronization
- **Slack Notifications** - Instant alerts for new reviews
- **Scheduled Updates** - Automated daily review collection
- **Preview Panel** - Quick view of latest 5 reviews
- **Error Handling** - Robust error management and reporting

## 🛠️ Technical Stack

- **Python 3.11** - Core programming language
- **Streamlit** - Web interface framework
- **Google Sheets API** - Data storage and management
- **Google Play Scraper** - Review data collection
- **Pandas** - Data manipulation and analysis
- **Slack Webhooks** - Notification system

## 🚀 Setup Instructions

### Prerequisites

1. Python 3.11
2. Google Cloud Project with Sheets API enabled
3. Slack Workspace with Webhook configuration
4. Google Sheets Service Account

### Environment Variables

Configure the following environment variables:

```env
GOOGLE_SHEETS_ID=your_sheet_id
GOOGLE_SHEETS_CREDENTIALS=your_service_account_json
SLACK_WEBHOOK_URL=your_slack_webhook_url
```

### Installation Steps

1. Clone the repository:
```bash
git clone [your-repo-url]
cd play-store-review-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## 📊 Project Structure

```
├── app.py                 # Main Streamlit dashboard
├── config.py             # Configuration settings
├── review_scraper.py    # Play Store review scraping logic
├── sheets_manager.py    # Google Sheets integration
└── scheduler.py         # Scheduled job management
```

## 💡 Usage Guide

1. **Dashboard Overview**
   - System status monitoring
   - Manual review update trigger
   - Latest reviews preview
   - Configuration status

2. **Automated Updates**
   - Reviews are automatically fetched daily at midnight
   - Schedule can be configured in `config.py`

3. **Slack Notifications**
   - Receive instant notifications for new reviews
   - Configurable notification format
   - Real-time update alerts

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

## 📝 Development Guidelines

1. Follow PEP 8 style guide
2. Add unit tests for new features
3. Update documentation as needed
4. Maintain error handling consistency
5. Keep the code modular and clean

## 🔒 Security

- All sensitive credentials are managed through environment variables
- API access is secured through service account authentication
- No sensitive data is logged or exposed in the UI

## 📫 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.