# 🚀 EngageMeter - Social Media Engagement Analytics

> **Track, analyze, and optimize your social media engagement with intelligent scoring and insights**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![HTMX](https://img.shields.io/badge/HTMX-1.9+-orange.svg)](https://htmx.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.0+-blue.svg)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 What is EngageMeter?

EngageMeter is a powerful social media engagement analytics platform that helps content creators, social media managers, and brands optimize their social media strategy through intelligent engagement scoring and data-driven insights.

### ✨ Key Features

- **🔐 Secure Authentication**: Email/password authentication with session management
- **📊 CSV Data Import**: Intelligent parsing of X Analytics and other platform exports
- **🎯 Engagement Scoring**: Configurable point values for likes, retweets, replies, and mentions
- **📈 Advanced Dashboard**: Real-time sorting, filtering, and analytics visualization
- **⚙️ Smart Settings**: Dynamic point value configuration with strategy optimization
- **📱 Responsive Design**: Mobile-first interface with HTMX-powered interactions
- **🔍 X Analytics Support**: Native support for X Analytics account overview and tweet-level data

### 🏗️ Architecture

- **Backend**: FastAPI with async/await support
- **Frontend**: HTMX + Tailwind CSS for dynamic interactions
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Local session-based auth with bcrypt hashing
- **File Processing**: Intelligent CSV parsing with format detection
- **Scoring Engine**: Configurable engagement scoring algorithm

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/engagemeter.git
cd engagemeter

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`

### Quick Demo

1. **Register** a new account
2. **Upload** your X Analytics CSV export
3. **Configure** engagement point values
4. **View** your engagement analytics dashboard
5. **Optimize** your strategy based on insights

## 📚 Documentation

- **[📖 Setup Guide](docs/SETUP_GUIDE.md)** - Complete installation and configuration
- **[👥 User Guide](docs/USER_GUIDE.md)** - How to use EngageMeter effectively
- **[🔌 API Reference](docs/API_REFERENCE.md)** - Complete API documentation
- **[🚀 Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment instructions

## 🎨 Screenshots

### Dashboard

![Dashboard](docs/screenshots/dashboard.png)

### Settings

![Settings](docs/screenshots/settings.png)

### Upload

![Upload](docs/screenshots/upload.png)

## 🔧 Development

### Project Structure

```
engagemeter/
├── app/                    # Main application code
│   ├── models.py          # Pydantic data models
│   ├── db.py              # Database operations
│   ├── auth.py            # Authentication logic
│   ├── scoring.py         # Engagement scoring engine
│   ├── csv_parser.py      # CSV parsing and validation
│   ├── routes/            # API route handlers
│   └── templates/         # HTML templates
├── docs/                  # Documentation
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test categories
pytest -k test_auth_system
pytest -k test_csv_parsing
pytest -k test_scoring_logic
pytest -k test_dashboard_core
```

### Development Server

```bash
# Start with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start with specific settings
uvicorn app.main:app --reload --env-file .env
```

## 📊 Project Status

- **MVP Completion**: 91.9% (34/37 points)
- **Current Sprint**: Final documentation and deployment
- **Next Milestone**: Production deployment

### Completed Features ✅

- [x] **T01**: User authentication system
- [x] **T02**: CSV import and parsing
- [x] **T03**: Engagement scoring engine
- [x] **T04**: Advanced dashboard UI
- [x] **T05**: User settings management
- [x] **T06**: UI design system and mockups

### In Progress 🔄

- [ ] **T07**: Documentation and deployment guide

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **HTMX** for seamless dynamic interactions
- **Tailwind CSS** for beautiful, responsive design
- **SQLAlchemy** for robust database operations

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/engagemeter/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/engagemeter/issues)
- **Email**: support@engagemeter-analytics.com

---

**Made with ❤️ for social media creators everywhere**
