# Twitter OAuth Setup Guide

This guide explains how to set up Twitter OAuth 2.0 for the Koe application.

## Prerequisites

1. A Twitter Developer Account
2. A Twitter App created in the Twitter Developer Portal
3. Python 3.8+ installed

## Twitter App Configuration

### 1. Create a Twitter App

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new app or use an existing one
3. Navigate to "App settings" > "Authentication settings"

### 2. Configure OAuth 2.0 Settings

- **App permissions**: Read
- **Type of App**: Web App
- **Callback URL**: `http://localhost:8000/auth/callback` (for development)
- **Website URL**: `http://localhost:8000` (for development)

### 3. Get Your Credentials

- **Client ID**: Found in "App settings" > "Keys and tokens"
- **Client Secret**: Found in "App settings" > "Keys and tokens"

## Environment Configuration

Create a `.env` file in your project root with the following variables:

```bash
# Twitter OAuth Configuration
TWITTER_CLIENT_ID=your_twitter_client_id_here
TWITTER_CLIENT_SECRET=your_twitter_client_secret_here
TWITTER_REDIRECT_URI=http://localhost:8000/auth/callback

# Database Configuration
DATABASE_URL=sqlite:///./app.db

# Security
SECRET_KEY=your_secret_key_here
```

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
uvicorn app.main:app --reload
```

3. Navigate to `http://localhost:8000/auth/login`

## OAuth Flow

1. **User clicks "Sign in with Twitter"**

   - Generates PKCE code verifier and challenge
   - Creates OAuth state parameter
   - Redirects to Twitter with authorization request

2. **Twitter redirects back to callback**
   - Verifies state parameter
   - Exchanges authorization code for access token
   - Fetches user information from Twitter
   - Creates or updates user in database
   - Redirects to dashboard

## Security Features

- **PKCE (Proof Key for Code Exchange)**: Prevents authorization code interception
- **State Parameter**: Prevents CSRF attacks
- **Secure Token Storage**: Tokens stored in SQLite database
- **Token Expiration**: Automatic token expiration handling

## Testing

Run the OAuth tests:

```bash
pytest -k test_oauth_flow
```

## Production Considerations

1. **HTTPS**: Always use HTTPS in production
2. **Environment Variables**: Store sensitive data in environment variables
3. **Database Security**: Use a production-grade database
4. **Session Management**: Implement proper session management
5. **Rate Limiting**: Add rate limiting to OAuth endpoints
6. **Logging**: Add comprehensive logging for security events

## Troubleshooting

### Common Issues

1. **"Invalid redirect URI" error**

   - Ensure callback URL matches exactly in Twitter app settings
   - Check for trailing slashes or protocol mismatches

2. **"Invalid client" error**

   - Verify TWITTER_CLIENT_ID and TWITTER_CLIENT_SECRET
   - Ensure app is approved and active

3. **"Invalid state parameter" error**
   - Check if OAuth state is being properly stored and retrieved
   - Verify database connection and table creation

### Debug Mode

Enable debug logging by setting:

```bash
export PYTHONPATH=.
export LOG_LEVEL=DEBUG
```

## API Endpoints

- `GET /auth/login` - Display login page
- `GET /auth/twitter/authorize` - Initiate OAuth flow
- `GET /auth/callback` - Handle OAuth callback
- `GET /auth/logout` - Logout user

## Database Schema

The OAuth implementation creates the following tables:

- `users` - User information and tokens
- `oauth_states` - OAuth state and code verifier storage
- `tweet_engagements` - Tweet engagement data (for future use)
