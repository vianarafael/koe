# Development Tickets

**Total Points:** 71 (MVP: 31 + Sprint 2: 26 + Epic Transformation: 14)

**Note:** This represents the transformation from Koe (passive dashboard) to EngageMeter (active strategy assistant with monetization focus).

## 🚀 **EPIC ROADMAP: Koe → EngageMeter Transformation**

### **EPIC A: Global Rename & Branding**

- **A1**: Codebase rename & branding (Koe → EngageMeter)
- **A2**: URL & meta updates

### **EPIC B: Data Consistency & Scoring**

- **B1**: CSV ingestion & schema sanity (X Analytics format)
- **B2**: Custom scoring rules (user-defined weights)
- **B3**: Metric math correctness
- **B4**: Engagement rate & funnels

### **EPIC C: Goals System Enhancement**

- **C1**: Monetization template (multi-goal with progress bars)
- **C2**: Custom goals & templates
- **C3**: Goal validation coach

### **EPIC D: Dashboard UX (DaisyUI + HTMX)**

- **D1**: Layout structure (Navbar + Sidebar + Content)
- **D2**: Empty states & value clarity
- **D3**: Tooltips & help text

### **EPIC E: Insights & Recommendations**

- **E1**: Insights engine v1 (rule-based)
- **E2**: Recommendations v1 (actionable)
- **E3**: Progress tracker

### **EPIC F: Onboarding & Upload Flow**

- **F1**: First-time upload (free tier)
- **F2**: CSV re-upload & overwrite

### **EPIC G: Paywall & Plans**

- **G1**: Pricing & gating (Free/Pro/Team)
- **G2**: Checkout integration (Stripe)
- **G3**: One-off report purchase

### **EPIC H: Landing Page**

- **H1**: One-pager (DaisyUI)

### **EPIC I: Settings & Account**

- **I1**: Scoring rules UI
- **I2**: Goals management
- **I3**: Data export

### **EPIC J: Reliability, Privacy, Tests**

- **J1**: Input validation & errors
- **J2**: Privacy note
- **J3**: Unit & e2e tests

---

## 🤖 **LLM Tickets (Current Sprint)**

**Points:** 5 | **Owner:** LLM

Create backend FastAPI endpoints and HTML templates with HTMX for user registration and login using email/password, securely store user accounts in SQLite database with password hashing. Inputs: email and password from registration/login forms; Outputs: user session and stored account. (acceptance_check: User can create account, login, and access protected endpoints with secure password storage.)

**Files to touch:**

- `app/auth.py`
- `app/templates/auth.html`
- `app/models.py`
- `app/db.py`

**Tests to run:**

- `pytest -k test_auth_system`

**Dependencies:**

---

### T02: Implement CSV import for X Analytics data

**Points:** 8 | **Owner:** LLM

Implement backend logic to parse X Analytics CSV files that users download from Twitter/X, extract engagement counts (likes, retweets, replies, mentions), and store data in SQLite with timestamp. Inputs: uploaded CSV file; Outputs: stored TweetEngagement records. (acceptance_check: CSV files are parsed correctly and engagement data is stored in database.)

**Files to touch:**

- `app/csv_parser.py`
- `app/models.py`
- `app/db.py`
- `app/templates/upload.html`

**Tests to run:**

- `pytest -k test_csv_parsing`

**Dependencies:**

- T01

---

### T03: Calculate engagement scores based on configurable point values

**Points:** 5 | **Owner:** LLM

Implement backend scoring logic that multiplies engagement counts by user-defined point values and stores engagement_score in database. Inputs: TweetEngagement data and user point values; Outputs: updated engagement_score field. (acceptance_check: engagement_score is correctly calculated for sample data.)

**Files to touch:**

- `app/scoring.py`
- `app/models.py`
- `app/db.py`

**Tests to run:**

- `pytest -k test_scoring_logic`

**Dependencies:**

- T02

---

### T04: Build dashboard UI to display tweets sorted by engagement score

**Points:** 8 | **Owner:** LLM

Create HTML templates with HTMX for dynamic interactions to display tweets with engagement metrics and scores, support sorting and filtering by engagement score. Inputs: EngagementDashboardResponse API data; Outputs: rendered dashboard UI. (acceptance_check: Dashboard renders tweets with correct scores and updates on data change.)

**Files to touch:**

- `app/templates/dashboard.html`
- `app/routes/dashboard.py`

**Tests to run:**

- `pytest -k test_dashboard_render`

**Dependencies:**

- T03

---

### T05: Implement user settings to update point values

**Points:** 5 | **Owner:** LLM

Add HTML templates with HTMX and backend API endpoints to allow users to set custom point values for likes, retweets, replies, and mentions, triggering recalculation of engagement scores. Inputs: SetPointValuesRequest; Outputs: updated user settings and recalculated scores. (acceptance_check: Updated point values affect engagement score calculations immediately.)

**Files to touch:**

- `app/templates/settings.html`
- `app/routes/settings.py`
- `app/scoring.py`

**Tests to run:**

- `pytest -k test_settings_update`

**Dependencies:**

- T03

---

## 👤 Human Tickets

### T06: [HUMAN] Design simple UI mockups for authentication, dashboard, and settings

**Points:** 3 | **Owner:** HUMAN

Create wireframes or sketches for authentication flow, dashboard displaying engagement scores, and settings page for point values to guide frontend implementation. (acceptance_check: Mockups approved and shared with frontend developer.)

---

### T07: [HUMAN] Write documentation for setup, usage, and API endpoints

**Points:** 3 | **Owner:** HUMAN

Prepare README and user guide covering project setup, usage instructions, and API endpoint descriptions for MVP. (acceptance_check: Documentation is complete and reviewed.)

---

## 🚀 **Sprint 2: Strategy Assistant Features**

_Note: These are not original tickets but represent the strategic pivot from passive data dashboard to active growth coach. This sprint transforms Koe into an actionable strategy assistant._

### T08: Implement goal setting system for engagement targets

**Points:** 8 | **Owner:** LLM

Create hybrid goal system with template-based defaults and custom goal creation. Implement 4 core goal categories with coaching validation and progress tracking. Primary focus on monetization path with multiple progress bars (impressions as hero, followers as supporting). Inputs: goal type selection, target customization, timeframe; Outputs: goal creation, progress calculation, coaching feedback, and burn-down style tracking. (acceptance_check: Users can choose from templates, set custom goals, receive coaching validation, and track progress with multiple metrics.)

**Files to touch:**

- `app/models.py` (add UserGoal, GoalTemplate, GoalProgress models)
- `app/db.py` (add goal CRUD operations and progress calculation)
- `app/routes/goals.py` (new goal management endpoints with coaching logic)
- `app/templates/goals.html` (goal setting interface with template selection)
- `app/templates/dashboard.html` (add goal progress display at top)
- `app/templates/index.html` (add goal progress above engagement score)

**Tests to run:**

- `pytest -k test_goal_system`

**Dependencies:**

- T01-T07 (MVP complete)

---

### T09: Implement X Analytics CSV Schema & Data Consistency

**Points:** 8 | **Owner:** LLM

Update CSV parser to handle X Analytics format with columns: Date, Impressions, Likes, Engagements, Bookmarks, Shares, New follows, Unfollows, Replies, Reposts, Profile visits, Create Post, Video views, Media views. Implement proper data types, date normalization, and schema validation. Inputs: X Analytics CSV format; Outputs: validated daily aggregates with proper typing. (acceptance_check: CSV uploads work with X Analytics format, data is properly typed, and validation provides helpful errors.)

**Files to touch:**

- `app/csv_parser.py` (update for X Analytics schema)
- `app/models.py` (add new engagement metrics)
- `app/db.py` (update database schema)
- `app/routes/upload.py` (enhance validation)

**Tests to run:**

- `pytest -k test_x_analytics_parsing`

**Dependencies:**

- T08

---

### T10: Implement Custom Scoring Rules & Weight System

**Points:** 6 | **Owner:** LLM

Create user-configurable scoring system where users can set custom weights for different engagement types (e.g., Like=1, Retweet=2, Reply=3, Mention=1). Include live preview of score impact and immediate recalculation. Inputs: user-defined weights; Outputs: updated scoring system with live preview. (acceptance_check: Users can customize scoring weights, see immediate impact on scores, and weights persist per user.)

**Files to touch:**

- `app/scoring.py` (enhance with custom weights)
- `app/models.py` (add scoring rules models)
- `app/templates/settings.html` (scoring weight UI)
- `app/routes/settings.py` (scoring rules endpoints)

**Tests to run:**

- `pytest -k test_custom_scoring`

**Dependencies:**

- T09

**Goal Templates:**

- 📈 Grow Impressions: 100K → 500K → 1M impressions/month
- 👥 Grow Followers: +100 → +500 → +1000 followers/month
- 💬 Boost Engagement: 50 → 200 → 500 replies/month
- 💵 Monetization Path: 5M impressions in 3 months + 500 verified followers (primary + secondary)

---

### T09: Build actionable insights engine based on real data patterns

**Points:** 6 | **Owner:** LLM

Implement insights engine that analyzes actual engagement data to provide actionable recommendations, not hardcoded advice. Focus on engagement trends, content productivity, and growth patterns. Inputs: user engagement data and historical patterns; Outputs: data-driven insights and strategy recommendations. (acceptance_check: Insights are based on actual data analysis, not assumptions, and provide actionable next steps.)

**Files to touch:**

- `app/insights.py` (new insights engine)
- `app/models.py` (add insight models)
- `app/routes/dashboard.py` (integrate insights)
- `app/templates/dashboard.html` (display insights)

**Tests to run:**

- `pytest -k test_insights_engine`

**Dependencies:**

- T08

---

### T10: Create growth analytics and trend analysis system

**Points:** 7 | **Owner:** LLM

Build analytics system for historical comparison, trend analysis, and performance benchmarking. Include engagement rate trends, content productivity metrics, and growth pattern identification. Inputs: historical engagement data and time-series analysis; Outputs: trend reports, growth metrics, and performance insights. (acceptance_check: Users can see performance trends, compare periods, and identify growth patterns.)

**Files to touch:**

- `app/analytics.py` (new analytics engine)
- `app/models.py` (add analytics models)
- `app/routes/analytics.py` (new analytics endpoints)
- `app/templates/analytics.html` (analytics dashboard)

**Tests to run:**

- `pytest -k test_analytics_system`

**Dependencies:**

- T09

---

### T11: Implement content optimization recommendations

**Points:** 5 | **Owner:** LLM

Create content optimization engine that identifies what drives engagement and recommends specific actions. Focus on content type analysis, posting patterns, and A/B testing suggestions based on actual performance data. Inputs: content performance data and engagement patterns; Outputs: specific recommendations for content improvement and testing strategies. (acceptance_check: Users receive specific, actionable content recommendations based on their data.)

**Files to touch:**

- `app/optimization.py` (new optimization engine)
- `app/models.py` (add optimization models)
- `app/routes/dashboard.py` (integrate recommendations)
- `app/templates/dashboard.html` (display recommendations)

**Tests to run:**

- `pytest -k test_optimization_engine`

**Dependencies:**

- T10

---

## 📊 **Sprint 2 Summary**

**Total Points:** 26
**Focus:** Transform Koe from passive data viewer to active growth coach
**Key Outcome:** Users get actionable insights and track progress toward engagement goals
**Strategic Value:** Differentiate from competitors by providing strategy, not just data
