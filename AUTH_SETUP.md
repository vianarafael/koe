# Email/Password Authentication Setup Guide

This guide explains how to set up and use the email/password authentication system for the Koe application.

## Prerequisites

1. Python 3.8+ installed
2. pip package manager

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
uvicorn app.main:app --reload
```

3. Navigate to `http://localhost:8000`

## Features

### User Registration

- Users can create accounts with email, username, and password
- Password must be at least 8 characters long
- Email and username must be unique
- Passwords are securely hashed using bcrypt

### User Login

- Users can sign in with email and password
- Secure session management with cookies
- Automatic redirect to dashboard after login

### Security Features

- Password hashing with bcrypt
- Session-based authentication
- Secure cookie settings
- Input validation and sanitization

## Usage

### 1. Create an Account

1. Navigate to `/auth/register`
2. Fill in your email, username, and password
3. Click "Create account"
4. You'll be automatically logged in and redirected to the dashboard

### 2. Sign In

1. Navigate to `/auth/login`
2. Enter your email and password
3. Click "Sign in"
4. You'll be redirected to the dashboard

### 3. Access Protected Content

- Once logged in, you'll see a welcome message
- Navigation will show Profile and Logout options
- Dashboard content changes based on authentication status

### 4. Sign Out

1. Click "Logout" in the navigation
2. Your session will be cleared
3. You'll be redirected to the home page

## API Endpoints

- `GET /auth/login` - Display login page
- `POST /auth/login` - Handle login form submission
- `GET /auth/register` - Display registration page
- `POST /auth/register` - Handle registration form submission
- `GET /auth/logout` - Logout user and clear session
- `GET /auth/profile` - Get current user profile (authenticated only)

## Database Schema

The authentication system creates the following tables:

- `users` - User accounts with email, username, hashed password, and point values
- `tweet_engagements` - Engagement data (for future use)

## Testing

Run the authentication tests:

```bash
pytest -k test_auth_system
```

## Configuration

Environment variables in `.env`:

```bash
# Database Configuration
DATABASE_URL=sqlite:///./app.db

# Security
SECRET_KEY=your_secret_key_here
SESSION_SECRET_KEY=your-session-secret-key-here
SESSION_COOKIE_NAME=koe_session
SESSION_COOKIE_SECURE=false  # Set to true in production with HTTPS
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=lax
```

## Production Considerations

1. **HTTPS**: Always use HTTPS in production
2. **Environment Variables**: Store sensitive data in environment variables
3. **Database Security**: Use a production-grade database
4. **Session Storage**: Consider using Redis for session storage in production
5. **Rate Limiting**: Add rate limiting to authentication endpoints
6. **Logging**: Add comprehensive logging for security events
7. **Password Policy**: Consider implementing stronger password requirements

## Troubleshooting

### Common Issues

1. **"Email already registered" error**

   - Use a different email address
   - Check if the email exists in the database

2. **"Username already taken" error**

   - Choose a different username
   - Usernames must be unique

3. **"Password must be at least 8 characters long" error**

   - Ensure password meets minimum length requirement

4. **Session not persisting**
   - Check cookie settings
   - Ensure browser accepts cookies
   - Check if session storage is working

### Debug Mode

Enable debug logging by setting:

```bash
export PYTHONPATH=.
export LOG_LEVEL=DEBUG
```

## Next Steps

After setting up authentication, you can proceed to:

1. **T02**: Implement CSV import for engagement data
2. **T03**: Calculate engagement scores
3. **T04**: Build dashboard UI
4. **T05**: Implement user settings

The authentication system provides the foundation for all subsequent features.
