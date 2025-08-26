# 🚀 Deployment Guide - EngageMeter

> **Complete production deployment guide for EngageMeter Social Media Analytics**

## 🎯 Overview

This guide covers deploying EngageMeter to production environments, including server setup, security configuration, performance optimization, and ongoing maintenance.

## 🏗️ Deployment Options

### Option 1: Traditional VPS/Cloud Server

- **Pros**: Full control, customizable, cost-effective
- **Cons**: Requires server management knowledge
- **Best for**: Developers, small teams, custom requirements

### Option 2: Platform as a Service (PaaS)

- **Pros**: Easy deployment, managed infrastructure, auto-scaling
- **Cons**: Less control, potential vendor lock-in
- **Best for**: Quick deployment, small to medium applications

### Option 3: Container Orchestration (Kubernetes)

- **Pros**: Scalable, portable, modern architecture
- **Cons**: Complex setup, requires expertise
- **Best for**: Large-scale deployments, microservices

## 🖥️ Server Requirements

### Minimum Requirements

- **CPU**: 2 vCPUs
- **RAM**: 4GB
- **Storage**: 20GB SSD
- **OS**: Ubuntu 20.04 LTS or newer

### Recommended Requirements

- **CPU**: 4 vCPUs
- **RAM**: 8GB
- **Storage**: 50GB SSD
- **OS**: Ubuntu 22.04 LTS
- **Network**: 1Gbps connection

### Production Requirements

- **CPU**: 8+ vCPUs
- **RAM**: 16GB+
- **Storage**: 100GB+ SSD with backup
- **OS**: Ubuntu 22.04 LTS
- **Network**: 1Gbps+ with load balancer
- **Monitoring**: Application and server monitoring

## 🚀 Traditional VPS Deployment

### Step 1: Server Setup

#### Initial Server Configuration

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git build-essential python3 python3-pip python3-venv nginx

# Install Node.js (for frontend build tools if needed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install PostgreSQL (optional, for production database)
sudo apt install -y postgresql postgresql-contrib
```

#### User and Security Setup

```bash
# Create application user
sudo adduser engagemeter
sudo usermod -aG sudo engagemeter

# Switch to engagemeter user
su - engagemeter

# Generate SSH key for secure access
ssh-keygen -t ed25519 -C "engagemeter-deployment"

# Add SSH key to authorized_keys
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

#### Firewall Configuration

```bash
# Configure UFW firewall
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Verify firewall status
sudo ufw status
```

### Step 2: Application Deployment

#### Clone and Setup Application

```bash
# Clone repository
git clone https://github.com/yourusername/engagemeter.git
cd engagemeter

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install production dependencies
pip install gunicorn uvicorn[standard]
```

#### Environment Configuration

```bash
# Create production environment file
cp .env.example .env.production

# Edit production environment
nano .env.production
```

**Production Environment Variables:**

```bash
# Application Settings
APP_NAME=EngageMeter Analytics
DEBUG=False
HOST=127.0.0.1
PORT=8000

# Database Configuration
DATABASE_URL=sqlite:///./engagemeter.db
# For PostgreSQL: DATABASE_URL=postgresql://engagemeter:password@localhost/engagemeter

# Security
SECRET_KEY=your-super-secure-production-secret-key
SESSION_SECRET_KEY=your-super-secure-session-key

# Session Configuration
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=strict

# Production Settings
WORKERS=4
WORKER_CLASS=uvicorn.workers.UvicornWorker
BIND=127.0.0.1:8000
```

#### Database Setup

```bash
# For SQLite (default)
# Database will be created automatically

# For PostgreSQL
sudo -u postgres createuser engagemeter
sudo -u postgres createdb engagemeter
sudo -u postgres psql -c "ALTER USER engagemeter PASSWORD 'your-secure-password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE engagemeter TO engagemeter;"
```

### Step 3: Process Management

#### Systemd Service Configuration

```bash
# Create systemd service file
sudo nano /etc/systemd/system/engagemeter.service
```

**Service Configuration:**

```ini
[Unit]
Description=EngageMeter Social Media Analytics
After=network.target

[Service]
Type=exec
User=engagemeter
Group=engagemeter
WorkingDirectory=/home/engagemeter/engagemeter
Environment=PATH=/home/engagemeter/engagemeter/.venv/bin
ExecStart=/home/engagemeter/engagemeter/.venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

#### Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable engagemeter

# Start service
sudo systemctl start engagemeter

# Check status
sudo systemctl status engagemeter

# View logs
sudo journalctl -u engagemeter -f
```

### Step 4: Nginx Configuration

#### Reverse Proxy Setup

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/engagemeter
```

**Nginx Configuration:**

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Client Max Body Size (for CSV uploads)
    client_max_body_size 10M;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Static Files (if any)
    location /static/ {
        alias /home/engagemeter/engagemeter/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Main Application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Health Check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

#### Enable Site and Test Configuration

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/engagemeter /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### Step 5: SSL Certificate

#### Let's Encrypt Setup

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

## ☁️ PaaS Deployment

### Heroku Deployment

#### Prerequisites

- Heroku account
- Heroku CLI installed
- Git repository

#### Deployment Steps

```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-engagemeter-app

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set SESSION_SECRET_KEY=your-session-key

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# Deploy application
git push heroku main

# Open application
heroku open
```

#### Heroku Configuration Files

**Procfile:**

```
web: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

**runtime.txt:**

```
python-3.11.0
```

### Railway Deployment

#### Prerequisites

- Railway account
- GitHub repository

#### Deployment Steps

1. **Connect GitHub repository** to Railway
2. **Set environment variables** in Railway dashboard
3. **Deploy automatically** on git push
4. **Configure custom domain** if needed

## 🐳 Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 engagemeter && chown -R engagemeter:engagemeter /app
USER engagemeter

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### Docker Compose

```yaml
version: "3.8"

services:
  engagemeter:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-secret-key
      - DATABASE_URL=sqlite:///./engagemeter.db
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - engagemeter
    restart: unless-stopped
```

## 🔒 Security Configuration

### Production Security Checklist

- [ ] **HTTPS enabled** with valid SSL certificate
- [ ] **Strong secret keys** generated and secured
- [ ] **Firewall configured** with minimal open ports
- [ ] **Regular security updates** enabled
- [ ] **Database security** configured
- [ ] **Session security** hardened
- [ ] **Rate limiting** implemented
- [ ] **Input validation** enforced
- [ ] **SQL injection protection** enabled
- [ ] **XSS protection** configured

### Security Headers

```nginx
# Add to Nginx configuration
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';";
add_header Referrer-Policy "strict-origin-when-cross-origin";
```

### Rate Limiting

```nginx
# Add to Nginx configuration
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=upload:10m rate=2r/s;

location /api/ {
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://127.0.0.1:8000;
}

location /upload/ {
    limit_req zone=upload burst=5 nodelay;
    proxy_pass http://127.0.0.1:8000;
}
```

## 📊 Performance Optimization

### Gunicorn Configuration

```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
```

### Nginx Optimization

```nginx
# Enable gzip compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

# Enable caching for static files
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Database Optimization

```sql
-- For SQLite
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = 10000;
PRAGMA temp_store = MEMORY;

-- For PostgreSQL
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
```

## 📈 Monitoring and Logging

### Application Monitoring

#### Health Check Endpoint

```python
# Add to app/main.py
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
```

#### Logging Configuration

```python
# Add to app/main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("engagemeter.log"),
        logging.StreamHandler()
    ]
)
```

### Server Monitoring

#### System Monitoring

```bash
# Install monitoring tools
sudo apt install -y htop iotop nethogs

# Monitor system resources
htop
iotop
nethogs
```

#### Log Monitoring

```bash
# Monitor application logs
sudo journalctl -u engagemeter -f

# Monitor Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Monitor system logs
sudo tail -f /var/log/syslog
```

## 🔄 Backup and Recovery

### Database Backup

```bash
# SQLite backup
cp /home/engagemeter/engagemeter/engagemeter.db /home/engagemeter/engagemeter/engagemeter.db.backup.$(date +%Y%m%d_%H%M%S)

# PostgreSQL backup
pg_dump engagemeter > engagemeter_backup_$(date +%Y%m%d_%H%M%S).sql

# Automated backup script
#!/bin/bash
BACKUP_DIR="/home/engagemeter/backups"
DATE=$(date +%Y%m%d_%H%M%S)
cp /home/engagemeter/engagemeter/engagemeter.db "$BACKUP_DIR/engagemeter_$DATE.db"
find "$BACKUP_DIR" -name "engagemeter_*.db" -mtime +7 -delete
```

### Application Backup

```bash
# Backup application code
tar -czf engagemeter_app_$(date +%Y%m%d_%H%M%S).tar.gz /home/engagemeter/engagemeter/

# Backup configuration files
sudo tar -czf engagemeter_config_$(date +%Y%m%d_%H%M%S).tar.gz /etc/nginx/sites-available/engagemeter /etc/systemd/system/engagemeter.service
```

## 🚨 Troubleshooting

### Common Issues

#### Application Won't Start

```bash
# Check service status
sudo systemctl status engagemeter

# Check logs
sudo journalctl -u engagemeter -f

# Check port availability
sudo netstat -tlnp | grep :8000

# Check file permissions
ls -la /home/engagemeter/engagemeter/
```

#### Nginx Issues

```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log

# Check Nginx status
sudo systemctl status nginx
```

#### Database Issues

```bash
# Check database file
ls -la /home/engagemeter/engagemeter/engagemeter.db

# Test database connection
python3 -c "from app.db import get_db; print('Database OK')"

# Check database permissions
sudo chown engagemeter:engagemeter /home/engagemeter/engagemeter/engagemeter.db
```

## 🔄 Maintenance

### Regular Maintenance Tasks

#### Weekly

- [ ] **Check logs** for errors
- [ ] **Monitor disk space** usage
- [ ] **Review security** updates
- [ ] **Test backup** restoration

#### Monthly

- [ ] **Update system** packages
- [ ] **Review performance** metrics
- [ ] **Check SSL certificate** expiration
- [ ] **Update application** dependencies

#### Quarterly

- [ ] **Security audit** review
- [ ] **Performance optimization** review
- [ ] **Backup strategy** review
- [ ] **Disaster recovery** testing

### Update Procedures

#### Application Updates

```bash
# Stop service
sudo systemctl stop engagemeter

# Backup current version
cp -r /home/engagemeter/engagemeter /home/engagemeter/engagemeter.backup.$(date +%Y%m%d)

# Pull latest changes
cd /home/engagemeter/engagemeter
git pull origin main

# Update dependencies
source .venv/bin/activate
pip install -r requirements.txt

# Restart service
sudo systemctl start engagemeter

# Check status
sudo systemctl status engagemeter
```

#### System Updates

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Restart services if needed
sudo systemctl restart nginx
sudo systemctl restart engagemeter
```

## 📚 Additional Resources

- **[Setup Guide](SETUP_GUIDE.md)**: Local development setup
- **[User Guide](USER_GUIDE.md)**: End-user documentation
- **[API Reference](API_REFERENCE.md)**: API documentation
- **[GitHub Repository](https://github.com/yourusername/engagemeter)**: Source code

---

**🚀 Your EngageMeter application is now ready for production! Monitor, maintain, and scale as needed.**
