# Source of Truth - Koe

## 🎯 Project Scope

- Track user engagement metrics (likes, retweets, replies, mentions) from uploaded CSV data
- Assign configurable point values to each interaction type
- Provide a simple dashboard summarizing engagement scores over time
- Allow users to view top-performing tweets by engagement score
- Support local user authentication with email/password
- Basic user onboarding and settings for point values
- CSV file upload and parsing for engagement data ingestion
- Intelligent CSV parsing with automatic column detection
- Automatic engagement score calculation using user-defined point values

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
- Intelligent CSV parsing that adapts to various export formats
- Automatic score calculation that adapts to user preferences

## 🔄 Key User Flows

1. User creates account with email and password
2. User signs in to access the dashboard
3. User uploads CSV files with engagement data (T02 ✅)
4. System automatically detects CSV column structure and parses data (T02 ✅)
5. User sets or accepts default point values for likes, retweets, replies, mentions (T03 ✅)
6. System parses CSV data and stores engagement metrics (T02 ✅)
7. System automatically calculates engagement scores per post using point values (T03 ✅)
8. User views dashboard with engagement scores and top posts (T03 ✅)
9. User updates point values and sees updated scores immediately

## 🏗️ Architecture

- Backend: FastAPI for API endpoints and authentication
- Frontend: HTMX with Tailwind CSS for dynamic interactions
- Database: SQLite for user accounts and engagement data
- Authentication: Local email/password with session management
- File Processing: CSV parsing for engagement data ingestion (T02 ✅)
- Scoring Engine: Automatic engagement score calculation (T03 ✅)
- Deployment: Linode server with direct deployment
- Session Management: In-memory session storage with secure cookies
- Development: Git push and manual server restart workflow
- CSV Processing: Intelligent column detection and data validation (T02 ✅)

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

- `id`: string (UUID, primary key)
- `tweet_id`: string
- `user_id`: string (foreign key)
- `tweet_text`: string (optional)
- `like_count`: integer
- `retweet_count`: integer
- `reply_count`: integer
- `mention_count`: integer
- `engagement_score`: integer (calculated using point values)
- `posted_date`: datetime (optional)
- `fetched_at`: datetime

### CSV Processing Models

- `CSVUploadResponse`: {'message': 'string', 'records_processed': 'integer', 'records_stored': 'integer', 'errors': ['string']}
- `CSVParseError`: {'row': 'integer', 'error': 'string', 'data': 'dict'}

### Scoring Models

- `SetPointValuesRequest`: {'like': 'integer', 'retweet': 'integer', 'reply': 'integer', 'mention': 'integer'}
- `PointValuesResponse`: {'message': 'string', 'updated_point_values': 'dict', 'recalculated_count': 'integer'}
- `EngagementScoreCalculation`: {'tweet_id': 'string', 'like_score': 'integer', 'retweet_score': 'integer', 'reply_score': 'integer', 'mention_score': 'integer', 'total_score': 'integer', 'calculation_details': 'dict'}

### API Input/Output

- `UserCreate`: {'email': 'string', 'username': 'string', 'password': 'string'}
- `UserLogin`: {'email': 'string', 'password': 'string'}
- `UserResponse`: {'id': 'string', 'email': 'string', 'username': 'string', 'point_values': 'dict', 'created_at': 'datetime'}
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

### CSV Upload System (T02 ✅)

- Users upload CSV files with engagement data
- System automatically detects column structure and maps to expected fields
- Support for various CSV formats from different platforms (X Analytics, etc.)
- Intelligent parsing with multiple date format support
- K/M suffix parsing for engagement numbers (e.g., "2.5K" → 2500)
- Data validation and error handling with detailed feedback
- Sample CSV download for user reference
- User data isolation and secure storage

### CSV Format Support

- **Required columns**: Tweet ID, Likes, Retweets, Replies
- **Optional columns**: Tweet text, Posted date, Mentions
- **Date formats**: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY, ISO timestamps
- **Number formats**: Plain integers, comma-separated, K/M suffixes

## 🎯 Scoring System (T03 ✅)

### Engagement Score Calculation

- **Formula**: `(likes × like_points) + (retweets × retweet_points) + (replies × reply_points) + (mentions × mention_points)`
- **Default Point Values**: Like(1), Retweet(2), Reply(3), Mention(1)
- **Automatic Calculation**: Scores calculated immediately upon CSV upload
- **User Customization**: Point values can be updated per user preferences

### Scoring Features

- **Real-time Calculation**: Scores computed and stored during data ingestion
- **Point Validation**: Ensures point values are non-negative integers
- **Score Recalculation**: Existing scores updated when point values change
- **Top Performers**: Dashboard highlights best-performing tweets by score
- **Score Ranges**: Database queries support score-based filtering and sorting

### Integration Points

- **CSV Upload**: Automatic scoring during file processing
- **Dashboard Display**: Shows current point values and calculated scores
- **Database Storage**: Engagement scores stored with engagement data
- **Performance Metrics**: Top engagements displayed by score ranking

## ✅ Definition of Done

- [x] User can create account and authenticate with email/password
- [x] System provides secure session management
- [x] User can access protected dashboard areas
- [x] Basic error handling for authentication and validation
- [x] System parses and stores CSV engagement data (T02 ✅)
- [x] CSV upload with intelligent column detection (T02 ✅)
- [x] File validation and error handling (T02 ✅)
- [x] User data isolation and storage (T02 ✅)
- [x] Engagement scores are calculated correctly based on point values (T03 ✅)
- [x] Automatic score calculation during CSV upload (T03 ✅)
- [x] Score calculation using configurable point values (T03 ✅)
- [x] Dashboard displays engagement scores and top performers (T03 ✅)
- [ ] User can update point values and see updated scores immediately
- [ ] Deployed and accessible via public URL
- [x] Automated tests cover key API endpoints and scoring logic (T03 ✅)

## 🚧 Current Status

### Completed (T01-T03)

- ✅ User authentication system (email/password)
- ✅ User registration and login
- ✅ Session management
- ✅ Protected routes and middleware
- ✅ Database schema for users
- ✅ Frontend templates with authentication
- ✅ Comprehensive test suite
- ✅ CSV parsing and data ingestion (T02 ✅)
- ✅ File upload handling and validation (T02 ✅)
- ✅ Engagement data storage and retrieval (T02 ✅)
- ✅ Intelligent CSV column detection (T02 ✅)
- ✅ Upload success messaging and error handling (T02 ✅)
- ✅ Engagement score calculation engine (T03 ✅)
- ✅ Automatic scoring during CSV upload (T03 ✅)
- ✅ Configurable point values with validation (T03 ✅)
- ✅ Dashboard score display and top performers (T03 ✅)
- ✅ Score-based database queries and sorting (T03 ✅)

### In Progress (T04)

- 🔄 Dashboard UI with advanced sorting/filtering by engagement score
- 🔄 Enhanced score visualization and analytics

### Planned (T05)

- 📋 User settings page for updating point values
- 📋 Real-time score updates and dashboard refresh
- 📋 Score recalculation triggers and notifications

## 🔧 Technical Implementation Details

### CSV Parser Features

- **Column Detection**: Automatically maps various column names (e.g., "Likes", "likes", "Like count")
- **Data Validation**: Ensures required fields are present and valid
- **Error Handling**: Tracks parsing errors with row numbers and context
- **Format Flexibility**: Supports multiple CSV export formats from different platforms
- **Performance**: Efficient parsing with minimal memory usage

### Scoring Engine Features

- **Mathematical Accuracy**: Precise score calculation using integer arithmetic
- **Point Validation**: Comprehensive validation of user-defined point values
- **Performance**: Efficient scoring for large datasets
- **Integration**: Seamless integration with CSV upload and database operations
- **Extensibility**: Easy to modify scoring algorithms and add new metrics

### Database Schema Updates

- **tweet_engagements table**: Stores all engagement data with proper indexing
- **User isolation**: Each user's data is completely separated
- **Data integrity**: Unique constraints prevent duplicate entries
- **Performance**: Optimized queries for dashboard display and score-based sorting
- **Score indexing**: Efficient queries for top performers and score ranges

### File Upload Security

- **File type validation**: Only CSV files accepted
- **Size limits**: Configurable file size restrictions
- **User authentication**: All uploads require valid session
- **Error feedback**: Clear messages for validation failures

### Dashboard Enhancements

- **Score Display**: Shows current engagement scores for all tweets
- **Point Values**: Displays current point values used for calculations
- **Top Performers**: Highlights best-performing tweets by score
- **Upload Feedback**: Indicates when scoring has been applied
- **Real-time Updates**: Scores calculated and displayed immediately
