# 🚀 EngageMeter.co - Super-Simple Analytics for Indie Hackers

> **Drop 1 snippet. Share our short link. See visits (last 24h).**

**Cheaper, faster, simpler than setting up Umami per project or paying Vercel Analytics**

Built for ship-fast indie hackers who want to track X → website → monetization funnels.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![HTMX](https://img.shields.io/badge/HTMX-1.9+-orange.svg)](https://htmx.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.0+-blue.svg)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 What is EngageMeter?

EngageMeter is a **super-simple analytics platform** that tracks your social media traffic to website conversions. Drop a tiny JS snippet, share our minified links, and see exactly which social posts drive traffic to your site.

**No more guessing** - know which social posts convert to website visits.

### ✨ MVP Features

- **🔧 One-Line Setup**: Tiny JS snippet to drop into your site
- **🏠 Multi-Site Support**: Track multiple domains/products from one account
- **🔗 Tracked Links**: Auto-generate short/minified URLs with UTMs
- **📊 24h Dashboard**: Bar graph of visits by source (X, Reddit, LinkedIn, Other)
- **🚀 Simple Management**: Add, delete, regenerate tracking links at will
- **🔒 Privacy-First**: No raw IPs stored, only hashed values

## 🏗️ Architecture

- **Backend**: FastAPI with async/await support
- **Frontend**: HTMX + DaisyUI (Tailwind CSS) for dynamic interactions
- **Database**: SQLite with aiosqlite
- **Authentication**: Local session-based auth with bcrypt hashing
- **Link Generation**: Short URL creation with UTM parameter tracking
- **Privacy**: SHA-256 hashing of IPs and User Agents, no PII storage

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
2. **Add your first site** (e.g., `mystartup.com`)
3. **Copy the JS snippet** and paste it into your website
4. **Create tracked links** for your URLs
5. **Share on social media** using the generated short URLs
6. **Monitor traffic** in your 24h dashboard

## 📊 How It Works

### 1. Add Your Site

Register your domain (e.g., `mystartup.com`) to get a unique tracking snippet.

### 2. Drop the Snippet

Add this single line to your website's `<head>` section:

```html
<script>
  !(function (d, w) {
    function sid() {
      try {
        return (
          localStorage.getItem("em_sid") ||
          (function () {
            const v = crypto.randomUUID();
            localStorage.setItem("em_sid", v);
            return v;
          })()
        );
      } catch (e) {
        return Math.random().toString(36).slice(2);
      }
    }
    function send() {
      const b = {
        path: location.pathname + location.search,
        referer: document.referrer || "",
        session_id: sid(),
        site_domain: EM_SITE,
      };
      if (navigator.sendBeacon) {
        navigator.sendBeacon(
          "/v1/ingest",
          new Blob([JSON.stringify(b)], { type: "application/json" })
        );
      } else {
        fetch("/v1/ingest", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(b),
          keepalive: true,
        }).catch(() => {});
      }
    }
    w.addEventListener("load", send);
  })(document, window);
</script>
```

**Note**: Replace `EM_SITE` with your actual domain when copying.

### 3. Create Tracked Links

- **Original**: `https://mystartup.com/pricing`
- **Generated**: `engmtr.co/abc123` (with UTM parameters)
- **Source**: X (Twitter)
- **Result**: Tracked click in your dashboard

### 4. Monitor Traffic

See exactly which social posts drive traffic:

- **X posts**: 45 visits in last 24h
- **Reddit comments**: 12 visits in last 24h
- **LinkedIn posts**: 8 visits in last 24h

## 🔧 Setup

### Site Management

1. **Add Site**: Enter your domain (e.g., `mystartup.com`)
2. **Copy Snippet**: Get your unique tracking code
3. **Paste**: Add to your website's `<head>` section

### Tracked Link Management

1. **Choose Site**: Select which domain to track
2. **Add URL**: Enter your website page URL
3. **Pick Source**: X, Reddit, LinkedIn, or Other
4. **Get Short Link**: Auto-generated with tracking parameters
5. **Share**: Use the short link in your social posts

## 📈 Dashboard Features

- **Site Management**: Add, edit, delete domains
- **Link Management**: Add, edit, delete tracking URLs
- **Source Breakdown**: X, Reddit, LinkedIn, Other
- **24h Traffic**: Bar graph of visits in last 24 hours
- **Simple Analytics**: Focus on what matters - traffic from social

## 🔒 Privacy & Security

- **No Raw IPs**: All IP addresses are SHA-256 hashed
- **No PII**: User agents and other identifiers are hashed
- **Domain Validation**: Can only track domains you own
- **Rate Limiting**: Prevents abuse and ensures performance
- **Session Tracking**: Uses first-party cookies for analytics

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
- [ ] **Multi-Site Support**: Track multiple domains
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
