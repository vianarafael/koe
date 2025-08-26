# 🚀 EngageMeter.co - Premium Funnel Tracker

> **Cheaper, faster, simpler than setting up Umami per project or paying Vercel Analytics**

Built for ship-fast indie hackers who want a funnel view from X → website → monetization.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![HTMX](https://img.shields.io/badge/HTMX-1.9+-orange.svg)](https://htmx.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.0+-blue.svg)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 What is EngageMeter?

EngageMeter is a **super-simple analytics platform** that tracks your social media traffic to website conversions. Drop a tiny JS snippet, share our minified links, and see exactly which X posts drive traffic to your site.

**No more guessing** - know which social posts convert to website visits.

### ✨ MVP Features

- **🔧 One-Line Setup**: Tiny JS snippet to drop into your site
- **🔗 Tracked Links**: Auto-generate short/minified URLs with UTMs
- **📊 24h Dashboard**: Bar graph of visits by source (X, Reddit, LinkedIn, Other)
- **🚀 Simple Management**: Add, delete, regenerate tracking links at will

## 🏗️ Architecture

- **Backend**: FastAPI with async/await support
- **Frontend**: HTMX + DaisyUI (Tailwind CSS) for dynamic interactions
- **Database**: SQLite with aiosqlite
- **Authentication**: Local session-based auth with bcrypt hashing
- **Link Generation**: Short URL creation with UTM parameter tracking

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
2. **Drop the JS snippet** into your website
3. **Create tracked links** for your URLs
4. **Share on social media** using the generated short URLs
5. **Monitor traffic** in your 24h dashboard

## 📊 How It Works

### 1. Drop the Snippet

```html
<script src="https://engagemeter.co/track.js"></script>
```

### 2. Create Tracked Links

- **Original**: `https://yoursite.com/pricing`
- **Generated**: `engmtr.co/abc123` (with UTM parameters)
- **Source**: X (Twitter)
- **Result**: Tracked click in your dashboard

### 3. Monitor Traffic

See exactly which social posts drive traffic:
- **X posts**: 45 visits in last 24h
- **Reddit comments**: 12 visits in last 24h
- **LinkedIn posts**: 8 visits in last 24h

## 🔧 Setup

### JS Tracking Snippet

Add this single line to your website's `<head>` section:

```html
<script src="https://engagemeter.co/track.js"></script>
```

### Tracked Link Management

1. **Add URL**: Enter your website page URL
2. **Pick Source**: X, Reddit, LinkedIn, or Other
3. **Get Short Link**: Auto-generated with tracking parameters
4. **Share**: Use the short link in your social posts

## 📈 Dashboard Features

- **Link Management**: Add, edit, delete tracking URLs
- **Source Breakdown**: X, Reddit, LinkedIn, Other
- **24h Traffic**: Bar graph of visits in last 24 hours
- **Simple Analytics**: Focus on what matters - traffic from social

## 🚀 Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
# Set environment variables
export DATABASE_URL="sqlite:///./engagemeter.db"
export SECRET_KEY="your-secret-key-here"

# Run with production server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🔧 Development

### Project Structure

```
engagemeter/
├── app/                    # Main application code
│   ├── models.py          # Pydantic data models
│   ├── db.py              # Database operations
│   ├── auth.py            # Authentication logic
│   ├── routes/            # API route handlers
│   └── templates/         # HTML templates
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
pytest -k test_link_tracking
pytest -k test_dashboard_core
```

## 📊 Project Status

- **MVP Status**: In Development
- **Current Focus**: Core tracking functionality
- **Next Milestone**: JS snippet and link generation

### Planned Features 🎯

- [ ] **JS Tracking Snippet**: One-line website integration
- [ ] **Link Management**: Create, edit, delete tracked URLs
- [ ] **Short URL Generation**: Auto-create minified links with UTMs
- [ ] **24h Dashboard**: Traffic visualization by source
- [ ] **Click Tracking**: Ingest pipeline for visitor data

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
- **DaisyUI** for beautiful, responsive design
- **SQLite** for simple, reliable data storage

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/engagemeter/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/engagemeter/issues)
- **Email**: support@engagemeter.co

---

**EngageMeter.co** - Simple analytics for indie hackers who ship fast.
