# Development Tickets

**Total Points:** 31

## 🤖 LLM Tickets

### T01: Implement simple email/password authentication system

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
