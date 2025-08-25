# 📖 Setup Guide - Koe

> **Complete installation and configuration guide for Koe Social Media Analytics**

## 🎯 Overview

This guide will walk you through setting up Koe on your local machine or server. Koe is designed to be easy to set up and get running quickly.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

### System Requirements

- **Operating System**: macOS 10.14+, Ubuntu 18.04+, Windows 10+ (WSL2 recommended)
- **Python**: 3.8 or higher
- **Memory**: Minimum 2GB RAM, 4GB+ recommended
- **Storage**: 1GB free space for application + data storage
- **Network**: Internet connection for dependency installation

### Required Software

- **Python 3.8+**: [Download from python.org](https://python.org/downloads/)
- **Git**: [Download from git-scm.com](https://git-scm.com/downloads)
- **pip**: Usually comes with Python, or install via [pip.pypa.io](https://pip.pypa.io/en/stable/installation/)

### Verify Installation

```bash
# Check Python version
python3 --version
# Should show Python 3.8.x or higher

# Check pip version
pip3 --version
# Should show pip version

# Check Git version
git --version
# Should show Git version
```

## 🚀 Installation Steps

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/koe.git

# Navigate to project directory
cd koe

# Verify the structure
ls -la
```

You should see:
```
koe/
├── app/
├── docs/
├── tests/
├── requirements.txt
├── README.md
└── ...
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Verify activation (should show path to .venv)
which python
```

### Step 3: Install Dependencies

```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

You should see packages like:
- fastapi
- uvicorn
- sqlalchemy
- passlib[bcrypt]
- jinja2
- python-multipart

### Step 4: Environment Configuration

```bash
# Create environment file
cp .env.example .env

# Edit environment variables
nano .env  # or use your preferred editor
```

#### Environment Variables

```bash
# Database Configuration
DATABASE_URL=sqlite:///./koe.db

# Security
SECRET_KEY=your-super-secret-key-here
SESSION_SECRET_KEY=your-session-secret-key-here

# Application Settings
APP_NAME=Koe Analytics
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Session Configuration
SESSION_COOKIE_NAME=koe_session
SESSION_COOKIE_SECURE=False  # Set to True in production
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=lax
```

### Step 5: Initialize Database

```bash
# The database will be created automatically on first run
# But you can also initialize it manually:

# Start Python shell
python3

# In Python shell:
from app.db import init_db
import asyncio

# Initialize database
asyncio.run(init_db())
print("Database initialized successfully!")
exit()
```

### Step 6: Run the Application

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the provided script
bash scripts/dev.sh
```

### Step 7: Verify Installation

1. **Open your browser** and navigate to `http://localhost:8000`
2. **You should see** the Koe landing page
3. **Click "Get Started"** to test the application
4. **Create an account** to verify authentication works

## 🔧 Configuration Options

### Database Configuration

Koe uses SQLite by default, but you can configure other databases:

```bash
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/koe

# MySQL
DATABASE_URL=mysql://user:password@localhost/koe

# SQLite (default)
DATABASE_URL=sqlite:///./koe.db
```

### Security Configuration

```bash
# Generate secure keys
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Use generated keys in .env
SECRET_KEY=your-generated-secret-key
SESSION_SECRET_KEY=your-generated-session-key
```

### Development vs Production

```bash
# Development (.env)
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Production (.env)
DEBUG=False
HOST=127.0.0.1
PORT=8000
```

## 🧪 Testing Your Setup

### Run the Test Suite

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run specific test categories
pytest -k test_auth_system
pytest -k test_csv_parsing
pytest -k test_scoring_logic
```

### Manual Testing

1. **Authentication Flow**
   - Register new account
   - Login with credentials
   - Test logout functionality

2. **CSV Upload**
   - Download sample CSV from upload page
   - Upload and verify parsing
   - Check engagement scores

3. **Dashboard Functionality**
   - View uploaded data
   - Test sorting and filtering
   - Verify score calculations

## 🚨 Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --reload --port 8001
```

#### Database Errors

```bash
# Remove existing database
rm koe.db

# Reinitialize
python3 -c "from app.db import init_db; import asyncio; asyncio.run(init_db())"
```

#### Import Errors

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Permission Errors

```bash
# Fix file permissions
chmod +x scripts/*.sh

# Fix directory permissions
chmod 755 app/ templates/ static/
```

### Getting Help

- **Check logs**: Look for error messages in terminal output
- **Verify Python version**: Ensure you're using Python 3.8+
- **Check dependencies**: Verify all packages are installed
- **GitHub Issues**: Search existing issues or create new ones

## 🔄 Updating Koe

### Update Dependencies

```bash
# Pull latest changes
git pull origin main

# Update virtual environment
source .venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Database Migrations

```bash
# Backup current database
cp koe.db koe.db.backup

# The application handles migrations automatically
# But you can also run them manually if needed
```

## 📱 Mobile Setup

### iOS/Android Testing

1. **Find your local IP address**
   ```bash
   # On macOS/Linux
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # On Windows
   ipconfig | findstr "IPv4"
   ```

2. **Run with host binding**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access from mobile device**
   - Navigate to `http://YOUR_LOCAL_IP:8000`
   - Test responsive design and touch interactions

## 🎉 Next Steps

After successful setup:

1. **Read the [User Guide](USER_GUIDE.md)** to learn how to use Koe
2. **Check the [API Reference](API_REFERENCE.md)** for developer information
3. **Review [Deployment Guide](DEPLOYMENT.md)** for production setup
4. **Join the community** and contribute to the project

---

**🎯 Setup complete! You're ready to start analyzing your social media engagement with Koe!**
