# 🔌 API Reference - EngageMeter

> **Complete API documentation for EngageMeter Social Media Analytics**

## 🎯 Overview

The EngageMeter API provides programmatic access to social media engagement analytics. All endpoints return JSON responses and support standard HTTP methods.

### Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

### Authentication

Most endpoints require authentication via session cookies. Include the session cookie in your requests:

```bash
# After login, include the session cookie
curl -H "Cookie: engagemeter_session=your-session-token" \
     http://localhost:8000/api/endpoint
```

## 🔐 Authentication Endpoints

### POST /auth/register

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "message": "Account created successfully",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "username": "username",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Status Codes:**
- `201`: Account created successfully
- `400`: Validation error (missing fields, invalid email, etc.)
- `409`: Email or username already exists

### POST /auth/login

Authenticate user and create session.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "username": "username",
    "point_values": {
      "like": 1,
      "retweet": 2,
      "reply": 3,
      "mention": 1
    }
  }
}
```

**Status Codes:**
- `200`: Login successful
- `401`: Invalid credentials
- `422`: Validation error

### POST /auth/logout

Terminate user session.

**Response:**
```json
{
  "message": "Logout successful"
}
```

**Status Codes:**
- `200`: Logout successful

### GET /auth/profile

Get current user profile information.

**Response:**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "username": "username",
  "point_values": {
    "like": 1,
    "retweet": 2,
    "reply": 3,
    "mention": 1
  },
  "created_at": "2024-01-15T10:30:00Z",
  "is_active": true
}
```

**Status Codes:**
- `200`: Profile retrieved successfully
- `401`: Not authenticated

## 📊 CSV Upload Endpoints

### GET /upload/

Get the CSV upload page (HTML).

**Response:** HTML page with upload form

### POST /upload/csv

Upload and process CSV file with engagement data.

**Request:** `multipart/form-data`
- `file`: CSV file (required)

**Response:**
```json
{
  "message": "CSV processed successfully",
  "records_processed": 150,
  "records_stored": 148,
  "errors": [
    {
      "row": 23,
      "error": "Invalid date format",
      "data": {"date": "invalid-date", "likes": "150"}
    }
  ]
}
```

**Status Codes:**
- `200`: Upload successful
- `400`: Invalid file format or parsing errors
- `401`: Not authenticated
- `422`: Validation errors

### GET /upload/sample-csv

Download sample CSV file for reference.

**Response:** CSV file download

## 🎯 Scoring and Settings Endpoints

### GET /settings/

Get the settings page (HTML).

**Response:** HTML page with settings form

### GET /settings/api/current-points

Get current user's point values.

**Response:**
```json
{
  "like": 1,
  "retweet": 2,
  "reply": 3,
  "mention": 1
}
```

**Status Codes:**
- `200`: Point values retrieved
- `401`: Not authenticated

### POST /settings/update-points

Update user's point values (JSON API).

**Request Body:**
```json
{
  "like": 2,
  "retweet": 4,
  "reply": 6,
  "mention": 2
}
```

**Response:**
```json
{
  "message": "Point values updated successfully",
  "updated_point_values": {
    "like": 2,
    "retweet": 4,
    "reply": 6,
    "mention": 2
  },
  "recalculated_count": 150
}
```

**Status Codes:**
- `200`: Update successful
- `400`: Invalid point values
- `401`: Not authenticated
- `422`: Validation errors

### POST /settings/update-points-htmx

Update point values with HTMX response.

**Request Body:** `application/x-www-form-urlencoded`
- `like`: Like point value
- `retweet`: Retweet point value
- `reply`: Reply point value
- `mention`: Mention point value

**Response:** HTML partial with updated settings

### GET /settings/api/point-impact

Analyze impact of current point values.

**Response:**
```json
{
  "current_values": {
    "like": 1,
    "retweet": 2,
    "reply": 3,
    "mention": 1
  },
  "scoring_formula": "(likes × 1) + (retweets × 2) + (replies × 3) + (mentions × 1)",
  "example_scenarios": {
    "high_engagement": {
      "likes": 100,
      "retweets": 25,
      "replies": 15,
      "mentions": 5,
      "total_score": 100 + 50 + 45 + 5
    },
    "medium_engagement": {
      "likes": 50,
      "retweets": 10,
      "replies": 8,
      "mentions": 2,
      "total_score": 50 + 20 + 24 + 2
    }
  },
  "recommendations": {
    "strategy": "Community-focused approach",
    "suggestions": [
      "Consider increasing reply points to encourage discussion",
      "Retweet points are balanced for reach",
      "Like points provide baseline engagement tracking"
    ]
  }
}
```

## 📈 Dashboard Endpoints

### GET /dashboard/

Get the main dashboard page (HTML).

**Response:** HTML page with dashboard

### GET /dashboard/api/engagements

Get engagement data with sorting and filtering.

**Query Parameters:**
- `sort_by`: Field to sort by (`score`, `date`, `likes`, `retweets`, `replies`)
- `sort_order`: Sort order (`asc`, `desc`)
- `min_score`: Minimum score filter
- `max_score`: Maximum score filter
- `limit`: Maximum number of results

**Response:**
```json
{
  "tweets": [
    {
      "id": "uuid-string",
      "tweet_id": "123456789",
      "tweet_text": "Sample tweet content",
      "like_count": 150,
      "retweet_count": 25,
      "reply_count": 12,
      "mention_count": 3,
      "engagement_score": 150 + 50 + 36 + 3,
      "posted_date": "2024-01-15T10:30:00Z",
      "fetched_at": "2024-01-15T11:00:00Z"
    }
  ],
  "total_count": 150,
  "filtered_count": 50
}
```

**Status Codes:**
- `200`: Data retrieved successfully
- `401`: Not authenticated

### GET /dashboard/api/stats

Get dashboard statistics and analytics.

**Response:**
```json
{
  "total_tweets": 150,
  "total_score": 7500,
  "average_score": 50.0,
  "top_score": 250,
  "engagement_breakdown": {
    "likes": {
      "total": 15000,
      "percentage": 60.0,
      "average_per_tweet": 100.0
    },
    "retweets": {
      "total": 5000,
      "percentage": 20.0,
      "average_per_tweet": 33.3
    },
    "replies": {
      "total": 3000,
      "percentage": 12.0,
      "average_per_tweet": 20.0
    },
    "mentions": {
      "total": 2000,
      "percentage": 8.0,
      "average_per_tweet": 13.3
    }
  },
  "score_distribution": {
    "0-10": 20,
    "11-25": 45,
    "26-50": 60,
    "51-100": 20,
    "100+": 5
  }
}
```

## 🏠 Home and Navigation

### GET /

Get the main landing page (HTML).

**Response:** HTML page with navigation and overview

## 📊 Data Models

### User

```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "username": "username",
  "hashed_password": "hashed-password-string",
  "point_values": {
    "like": 1,
    "retweet": 2,
    "reply": 3,
    "mention": 1
  },
  "created_at": "2024-01-15T10:30:00Z",
  "is_active": true
}
```

### TweetEngagement

```json
{
  "id": "uuid-string",
  "tweet_id": "123456789",
  "user_id": "user-uuid",
  "tweet_text": "Sample tweet content",
  "like_count": 150,
  "retweet_count": 25,
  "reply_count": 12,
  "mention_count": 3,
  "engagement_score": 239,
  "posted_date": "2024-01-15T10:30:00Z",
  "fetched_at": "2024-01-15T11:00:00Z"
}
```

### CSVUploadResponse

```json
{
  "message": "Upload successful",
  "records_processed": 150,
  "records_stored": 148,
  "errors": [
    {
      "row": 23,
      "error": "Invalid date format",
      "data": {"date": "invalid-date", "likes": "150"}
    }
  ]
}
```

### PointValuesResponse

```json
{
  "message": "Update successful",
  "updated_point_values": {
    "like": 2,
    "retweet": 4,
    "reply": 6,
    "mention": 2
  },
  "recalculated_count": 150
}
```

## 🔧 Error Handling

### Standard Error Response

```json
{
  "detail": "Error description",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Codes

- `AUTH_REQUIRED`: Authentication required
- `INVALID_CREDENTIALS`: Invalid login credentials
- `VALIDATION_ERROR`: Request validation failed
- `CSV_PARSE_ERROR`: CSV parsing failed
- `DATABASE_ERROR`: Database operation failed
- `FILE_TOO_LARGE`: Uploaded file exceeds size limit
- `INVALID_FILE_TYPE`: Unsupported file type

### HTTP Status Codes

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

## 📱 Client Examples

### Python Client

```python
import requests
import json

class EngageMeterClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def login(self, email, password):
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json={"email": email, "password": password}
        )
        return response.json()
    
    def get_engagements(self, **params):
        response = self.session.get(
            f"{self.base_url}/dashboard/api/engagements",
            params=params
        )
        return response.json()
    
    def update_point_values(self, like, retweet, reply, mention):
        response = self.session.post(
            f"{self.base_url}/settings/update-points",
            json={
                "like": like,
                "retweet": retweet,
                "reply": reply,
                "mention": mention
            }
        )
        return response.json()

# Usage
client = EngageMeterClient()
client.login("user@example.com", "password")
engagements = client.get_engagements(sort_by="score", limit=10)
```

### JavaScript Client

```javascript
class EngageMeterClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async login(email, password) {
        const response = await fetch(`${this.baseUrl}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
            credentials: 'include'
        });
        return response.json();
    }
    
    async getEngagements(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const response = await fetch(
            `${this.baseUrl}/dashboard/api/engagements?${queryString}`,
            { credentials: 'include' }
        );
        return response.json();
    }
    
    async updatePointValues(like, retweet, reply, mention) {
        const response = await fetch(`${this.baseUrl}/settings/update-points`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ like, retweet, reply, mention }),
            credentials: 'include'
        });
        return response.json();
    }
}

// Usage
const client = new EngageMeterClient();
client.login('user@example.com', 'password')
    .then(() => client.getEngagements({ sort_by: 'score', limit: 10 }))
    .then(data => console.log(data));
```

### cURL Examples

```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}' \
  -c cookies.txt

# Get engagements (using saved cookies)
curl -X GET "http://localhost:8000/dashboard/api/engagements?sort_by=score&limit=10" \
  -b cookies.txt

# Update point values
curl -X POST http://localhost:8000/settings/update-points \
  -H "Content-Type: application/json" \
  -d '{"like":2,"retweet":4,"reply":6,"mention":2}' \
  -b cookies.txt
```

## 🔒 Security Considerations

### Authentication

- All sensitive endpoints require authentication
- Sessions expire after inactivity
- Passwords are hashed using bcrypt
- CSRF protection via session validation

### Rate Limiting

- API endpoints are rate-limited to prevent abuse
- Upload endpoints have file size restrictions
- Session-based rate limiting per user

### Data Validation

- All input is validated using Pydantic models
- SQL injection protection via SQLAlchemy ORM
- File type validation for uploads
- XSS protection via proper HTML escaping

## 📚 Additional Resources

- **[Setup Guide](SETUP_GUIDE.md)**: Installation and configuration
- **[User Guide](USER_GUIDE.md)**: End-user documentation
- **[Deployment Guide](DEPLOYMENT.md)**: Production deployment
- **[GitHub Repository](https://github.com/yourusername/engagemeter)**: Source code and issues

---

**🔌 Ready to integrate with EngageMeter? Use these endpoints to build powerful social media analytics applications!**
