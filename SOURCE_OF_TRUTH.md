# Source of Truth - Koe

## 🎯 Project Scope

- Track user engagement metrics (likes, retweets, replies, mentions) from uploaded CSV data
- Assign configurable point values to each interaction type
- Provide a simple dashboard summarizing engagement scores over time
- Allow users to view top-performing tweets by engagement score
- Support local user authentication with email/password
- Basic user onboarding and settings for point values
- CSV file upload and parsing for engagement data ingestion

## ❌ Non-Goals

- Advanced analytics beyond engagement scoring (e.g., sentiment analysis)
- Scheduling or posting tweets
- Multi-account management
- Monetization features in MVP
- Mobile app (web only)
- Twitter API integration (using CSV uploads instead)

## 👥 Target Users

- Individual social media users seeking to optimize engagement
- Social media managers for small brands or personal brands
- Content creators wanting quick feedback on post performance
- Users who export engagement data from various platforms

## 💎 Value Propositions

- Quantify social media engagement with a simple point system
- Help users identify which content types generate the most engagement
- Enable data-driven content strategy optimization
- Lightweight, fast setup with minimal configuration
- No API dependencies or rate limits

## 🔄 Key User Flows

1. User creates account with email and password
2. User signs in to access the dashboard
3. User uploads CSV files with engagement data
4. User sets or accepts default point values for likes, retweets, replies, mentions
5. System parses CSV data and stores engagement metrics
6. System calculates engagement scores per post
7. User views dashboard with engagement scores and top posts
8. User updates point values and sees updated scores immediately

## 🏗️ Architecture

- Backend: FastAPI for API endpoints and authentication
- Frontend: HTMX with Tailwind CSS for dynamic interactions
- Database: SQLite for user accounts and engagement data
- Authentication: Local email/password with session management
- File Processing: CSV parsing for engagement data ingestion
- Deployment: Linode server with direct deployment
- Session Management: In-memory session storage with secure cookies
- Development: Git push and manual server restart workflow

## 📊 Data Contracts

### User

- `id`: string (UUID)
- `email`: string (unique)
- `username`: string (unique)
- `hashed_password`: string
- `point_values`: {'like': 'integer', 'retweet': 'integer', 'reply': 'integer', 'mention': 'integer'}
- `created_at`: datetime
- `is_active`: boolean

### TweetEngagement

- `tweet_id`: string
- `user_id`: string (foreign key)
- `like_count`: integer
- `retweet_count`: integer
- `reply_count`: integer
- `mention_count`: integer
- `engagement_score`: integer
- `fetched_at`: datetime

### API Input/Output

- `UserCreate`: {'email': 'string', 'username': 'string', 'password': 'string'}
- `UserLogin`: {'email': 'string', 'password': 'string'}
- `UserResponse`: {'id': 'string', 'email': 'string', 'username': 'string', 'point_values': 'dict', 'created_at': 'datetime'}
- `SetPointValuesRequest`: {'like': 'integer', 'retweet': 'integer', 'reply': 'integer', 'mention': 'integer'}
- `EngagementDashboardResponse`: {'tweets': [{'tweet_id': 'string', 'text': 'string', 'engagement_score': 'integer', 'like_count': 'integer', 'retweet_count': 'integer', 'reply_count': 'integer', 'mention_count': 'integer', 'created_at': 'datetime'}], 'total_score': 'integer'}

## 🔐 Authentication System

### Current Implementation

- Email/password registration and login
- Session-based authentication with secure cookies
- Password hashing using bcrypt
- Protected endpoints requiring authentication
- User profile management

### Security Features

- Secure password hashing
- Session management with expiration
- Input validation and sanitization
- CSRF protection through session validation

## 📁 Data Ingestion

### CSV Upload System

- Users upload CSV files with engagement data
- System parses and validates CSV format
- Data stored in SQLite database per user
- Support for various CSV formats from different platforms

## ✅ Definition of Done

- [x] User can create account and authenticate with email/password
- [x] System provides secure session management
- [x] User can access protected dashboard areas
- [x] Basic error handling for authentication and validation
- [ ] System parses and stores CSV engagement data
- [ ] Engagement scores are calculated correctly based on point values
- [ ] Dashboard displays posts sorted by engagement score
- [ ] User can update point values and see updated scores immediately
- [ ] Deployed and accessible via public URL
- [ ] Automated tests cover key API endpoints and scoring logic

## 🚧 Current Status

### Completed (T01)

- ✅ User authentication system (email/password)
- ✅ User registration and login
- ✅ Session management
- ✅ Protected routes and middleware
- ✅ Database schema for users
- ✅ Frontend templates with authentication
- ✅ Comprehensive test suite

### In Progress (T02)

- 🔄 CSV parsing and data ingestion
- 🔄 Engagement data storage
- 🔄 File upload handling

### Planned (T03-T05)

- 📋 Engagement score calculation
- 📋 Dashboard UI with sorting/filtering
- 📋 User settings for point values
- 📋 Score recalculation on updates
