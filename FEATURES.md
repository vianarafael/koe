# 🎯 EngageMeter.co - Feature Scope

This document defines what's **IN SCOPE** and **OUT OF SCOPE** for the EngageMeter.co MVP.

## 🚀 MVP Goal

**Super-simple analytics for indie hackers** who want to track X → website → monetization funnels.

**Tagline**: "Drop 1 snippet. Share our short link. See visits (last 24h)."

## ✅ IN SCOPE (MVP Features)

### 🔧 Core Setup

- [x] **User Authentication**: Email/password registration and login
- [x] **Session Management**: Secure user sessions
- [ ] **Multi-Site Support**: Track multiple domains/products from one account
- [ ] **JS Tracking Snippet**: One-line website integration with privacy-first design

### 🏠 Site Management

- [ ] **Site Registration**: Add domains (e.g., `mystartup.com`)
- [ ] **Domain Validation**: Prevent open redirects (only track owned domains)
- [ ] **Site Dashboard**: Overview per domain with unique tracking snippet
- [ ] **Site CRUD**: Create, edit, delete sites

### 🔗 Link Tracking

- [ ] **URL Management**: Add, edit, delete website URLs to track
- [ ] **Source Selection**: Pick traffic source (X, Reddit, LinkedIn, Other)
- [ ] **Short URL Generation**: Auto-create minified links (e.g., `engmtr.co/abc123`)
- [ ] **UTM Parameters**: Automatic UTM tagging for source tracking
- [ ] **Query Preservation**: Merge UTMs with existing query strings

### 📊 Analytics Dashboard

- [ ] **24h Traffic View**: Bar graph of visits in last 24 hours by hour
- [ ] **Source Breakdown**: Traffic by X, Reddit, LinkedIn, Other
- [ ] **Link Performance**: Show clicks per tracked URL
- [ ] **Simple Metrics**: Focus on traffic volume, not complex analytics
- [ ] **Real-time Updates**: HTMX-powered live dashboard

### 🔒 Privacy & Security

- [ ] **IP Hashing**: SHA-256 hash of IP addresses (no raw IPs stored)
- [ ] **UA Hashing**: SHA-256 hash of User Agents (no PII)
- [ ] **Rate Limiting**: Prevent abuse on redirect and ingest endpoints
- [ ] **Domain Validation**: Only allow tracking of owned domains
- [ ] **Session Tracking**: First-party cookies for analytics

### 🚀 Management

- [ ] **Link CRUD**: Create, read, update, delete tracking URLs
- [ ] **Regenerate Links**: Delete and recreate short URLs as needed
- [ ] **User Dashboard**: Simple overview of all tracked links
- [ ] **Copy Buttons**: Easy copying of snippets and short URLs

## ❌ OUT OF SCOPE (Not MVP)

### 🚫 CSV Import & Social Analytics

- [x] ~~CSV parsing and X Analytics support~~ (Remove)
- [x] ~~Engagement scoring engine~~ (Remove)
- [x] ~~Social media performance metrics~~ (Remove)
- [x] ~~Goal setting and progress tracking~~ (Remove)
- [x] ~~Best time to post analysis~~ (Remove)

### 🚫 Advanced Analytics

- [x] ~~Complex filtering and date ranges~~ (Remove)
- [x] ~~Engagement breakdowns~~ (Remove)
- [x] ~~Performance optimization suggestions~~ (Remove)
- [x] ~~Export functionality~~ (Remove)

### 🚫 Complex Features

- [x] ~~Multiple user roles~~ (Remove)
- [x] ~~Team collaboration~~ (Remove)
- [x] ~~API integrations~~ (Remove)
- [x] ~~Webhook support~~ (Remove)

## 🎯 MVP Success Criteria

### Must Have ✅

1. **User can register/login** with email/password
2. **User can add multiple sites** (domains) to track
3. **User can add website URLs** to track per site
4. **System generates short URLs** with UTM parameters
5. **JS snippet tracks visits** to user's site (privacy-first)
6. **Dashboard shows 24h traffic** by source with bar chart
7. **User can manage** (add/edit/delete) tracked links
8. **Source detection works** with and without UTMs

### Nice to Have 🎨

1. **Simple traffic graphs** (24h by hour)
2. **Click count per link**
3. **Basic user settings**
4. **Mobile-responsive design**
5. **Copy buttons** for snippets and URLs

### Future Features 🚀

1. **7d/30d time ranges**
2. **Conversion goal tracking**
3. **A/B testing support**
4. **Email notifications**
5. **API access for developers**

## 🔄 Migration Plan

### Phase 1: Remove Old Features

- [ ] Remove CSV upload functionality
- [ ] Remove engagement scoring
- [ ] Remove social media analytics
- [ ] Clean up old database tables
- [ ] Update navigation and UI

### Phase 2: Build New Core

- [ ] Create site management models and UI
- [ ] Create link tracking models and database schema
- [ ] Build short URL generation with UTM support
- [ ] Implement JS tracking snippet
- [ ] Create simple dashboard with 24h charts
- [ ] Add link management UI

### Phase 3: Polish & Deploy

- [ ] UI/UX improvements
- [ ] Testing and bug fixes
- [ ] Production deployment
- [ ] Documentation updates

## 📋 Technical Requirements

### Backend (Keep)

- [x] FastAPI framework
- [x] SQLite database
- [x] User authentication
- [x] Session management

### Backend (Add)

- [ ] **Site management models** (sites table)
- [ ] **Link tracking models** (tracked_links table)
- [ ] **Event tracking models** (events table)
- [ ] **Short URL generation** (base62 encoding)
- [ ] **Click ingestion API** (`/v1/ingest`)
- [ ] **Redirect handling** (`/{short_code}`)
- [ ] **Traffic aggregation** (24h by source)
- [ ] **Rate limiting** (leaky bucket)
- [ ] **Domain validation** (prevent open redirects)

### Frontend (Keep)

- [x] HTMX for interactions
- [x] DaisyUI components
- [x] Responsive design
- [x] User dashboard structure

### Frontend (Add)

- [ ] **Site management forms** (add/edit/delete sites)
- [ ] **Link management forms** (add/edit/delete links)
- [ ] **Traffic visualization** (24h bar charts)
- [ ] **Copy buttons** for snippets and URLs
- [ ] **Empty states** and user guidance

## 🗄️ Data Model Requirements

### Database Schema

```sql
-- Sites table
sites(id, user_id, domain, created_at)

-- Tracked links table
tracked_links(id, user_id, site_id, original_url, source, short_code, utm_source, utm_medium, utm_campaign, created_at, is_active)

-- Events table
events(id, tracked_link_id, site_id, user_id, kind, ts, ip_hash, ua_hash, referer, utm_source, utm_medium, utm_campaign, country, path, session_id)

-- Users table (existing)
users(id, email, password_hash, created_at)
```

### Key Relationships

- **User** → **Sites** (one-to-many)
- **Site** → **Tracked Links** (one-to-many)
- **Tracked Link** → **Events** (one-to-many)
- **Site** → **Events** (one-to-many)

### Indexes Required

- `events(ts)` - For time-based queries
- `events(site_id)` - For site-specific analytics
- `events(tracked_link_id)` - For link-specific analytics
- `tracked_links(short_code)` - For redirect lookups

## 🔍 Source Detection Logic

### Priority Order

1. **UTM Source** (if present in URL)
2. **Referrer Domain** mapping:
   - `twitter.com` / `t.co` → `x`
   - `linkedin.com` → `linkedin`
   - `reddit.com` → `reddit`
   - Else → `other`

### Implementation

```python
def infer_source(utm_source: str, referer: str) -> str:
    if utm_source:
        return utm_source

    # Parse referer domain and map
    domain = extract_domain(referer)
    return SOURCE_MAPPING.get(domain, 'other')
```

## 🚀 API Endpoints Required

### Core Endpoints

- `POST /sites` - Create new site
- `GET /sites` - List user's sites
- `POST /links` - Create tracked link
- `GET /links` - List tracked links
- `GET /{short_code}` - Redirect and track click
- `POST /v1/ingest` - Track pageview

### Dashboard Endpoints

- `GET /dashboard/sites` - Site management page
- `GET /dashboard/links` - Link management page
- `GET /dashboard/overview` - Analytics overview
- `GET /api/analytics/24h` - 24h traffic data

## 🎯 Why This Scope?

### **Focus on Core Value**

- **Simple**: One JS snippet, one dashboard
- **Fast**: Quick setup, immediate results
- **Clear**: Know which social posts drive traffic

### **Competitive Advantage**

- **Cheaper** than Vercel Analytics
- **Faster** than setting up Umami
- **Simpler** than Google Analytics
- **Focused** on indie hacker needs

### **Ship Fast Philosophy**

- **MVP first**: Core functionality only
- **Iterate later**: Add features based on user feedback
- **Stay lean**: Avoid feature creep and complexity

---

**Remember**: This is a pivot to a **completely different product**. We're building a funnel tracker, not a social media analytics tool.
