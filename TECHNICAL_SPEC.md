# 🛠️ EngageMeter.co - Technical Specification

This document provides detailed technical requirements for implementing the EngageMeter.co MVP.

## 🎯 MVP Overview

**Goal**: Build a super-simple analytics platform that tracks social media traffic to website conversions.

**Tagline**: "Drop 1 snippet. Share our short link. See visits (last 24h)."

## 🗄️ Database Schema

### Tables Required

#### 1. Sites Table

```sql
CREATE TABLE sites (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    domain TEXT NOT NULL,
    created_at TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

#### 2. Tracked Links Table

```sql
CREATE TABLE tracked_links (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    original_url TEXT NOT NULL,
    source TEXT NOT NULL CHECK (source IN ('x', 'reddit', 'linkedin', 'other')),
    short_code TEXT UNIQUE NOT NULL,
    utm_source TEXT NOT NULL,
    utm_medium TEXT NOT NULL DEFAULT 'social',
    utm_campaign TEXT NOT NULL DEFAULT 'link_tracking',
    created_at TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (site_id) REFERENCES sites (id)
);
```

#### 3. Events Table

```sql
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    tracked_link_id TEXT,
    site_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    kind TEXT NOT NULL CHECK (kind IN ('click', 'pageview')),
    ts TEXT NOT NULL,
    ip_hash TEXT,
    ua_hash TEXT,
    referer TEXT,
    utm_source TEXT,
    utm_medium TEXT,
    utm_campaign TEXT,
    country TEXT,
    path TEXT,
    session_id TEXT,
    FOREIGN KEY (tracked_link_id) REFERENCES tracked_links (id),
    FOREIGN KEY (site_id) REFERENCES sites (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### Indexes Required

```sql
CREATE INDEX idx_sites_user_id ON sites(user_id);
CREATE INDEX idx_tracked_links_user_id ON tracked_links(user_id);
CREATE INDEX idx_tracked_links_site_id ON tracked_links(site_id);
CREATE INDEX idx_tracked_links_short_code ON tracked_links(short_code);
CREATE INDEX idx_events_ts ON events(ts);
CREATE INDEX idx_events_site_id ON events(site_id);
CREATE INDEX idx_events_tracked_link_id ON events(tracked_link_id);
CREATE INDEX idx_events_session_id ON events(session_id);
```

## 🔗 API Endpoints

### Core Endpoints

#### 1. Site Management

- `POST /sites` - Create new site
- `GET /sites` - List user's sites
- `PUT /sites/{site_id}` - Update site
- `DELETE /sites/{site_id}` - Delete site

#### 2. Link Management

- `POST /links` - Create tracked link
- `GET /links` - List tracked links
- `PUT /links/{link_id}` - Update tracked link
- `DELETE /links/{link_id}` - Delete tracked link

#### 3. Tracking & Analytics

- `GET /{short_code}` - Redirect and track click
- `POST /v1/ingest` - Track pageview
- `GET /api/analytics/24h` - 24h traffic data by source

### Dashboard Routes

- `GET /dashboard/sites` - Site management page
- `GET /dashboard/links` - Link management page
- `GET /dashboard/overview` - Analytics overview

## 🔍 Source Detection Logic

### Priority Order

1. **UTM Source** (if present in URL query parameters)
2. **Referrer Domain** mapping:
   - `twitter.com` / `t.co` → `x`
   - `linkedin.com` → `linkedin`
   - `reddit.com` → `reddit`
   - Else → `other`

### Implementation

```python
SOURCE_MAPPING = {
    'twitter.com': 'x',
    't.co': 'x',
    'linkedin.com': 'linkedin',
    'reddit.com': 'reddit'
}

def infer_source(utm_source: str, referer: str) -> str:
    """Determine traffic source from UTM or referrer"""
    if utm_source:
        return utm_source

    if not referer:
        return 'other'

    # Extract domain from referrer
    domain = extract_domain(referer)
    return SOURCE_MAPPING.get(domain, 'other')
```

## 🔒 Privacy & Security

### Data Hashing

- **IP Addresses**: SHA-256 hash before storage
- **User Agents**: SHA-256 hash before storage
- **No Raw PII**: Only hashed values stored

### Rate Limiting

- **Redirect Endpoint**: 100 requests/minute per IP
- **Ingest Endpoint**: 1000 requests/minute per IP
- **Implementation**: Simple leaky bucket algorithm

### Domain Validation

- **Ownership Check**: Only allow tracking of domains user owns
- **Subdomain Support**: Allow tracking of subdomains
- **Prevent Open Redirects**: Validate original_url host matches site domain

## 📊 Analytics Queries

### 24h Traffic by Source

```sql
SELECT
    strftime('%H', ts) as hour,
    COALESCE(utm_source,
        CASE
            WHEN referer LIKE '%twitter.com%' OR referer LIKE '%t.co%' THEN 'x'
            WHEN referer LIKE '%linkedin.com%' THEN 'linkedin'
            WHEN referer LIKE '%reddit.com%' THEN 'reddit'
            ELSE 'other'
        END
    ) as source,
    COUNT(*) as visits
FROM events
WHERE site_id = ?
    AND ts >= datetime('now', '-24 hours')
    AND kind = 'pageview'
GROUP BY hour, source
ORDER BY hour, source;
```

### Click Tracking per Link

```sql
SELECT
    tl.original_url,
    tl.source,
    COUNT(e.id) as clicks_24h
FROM tracked_links tl
LEFT JOIN events e ON tl.id = e.tracked_link_id
    AND e.kind = 'click'
    AND e.ts >= datetime('now', '-24 hours')
WHERE tl.site_id = ? AND tl.is_active = 1
GROUP BY tl.id, tl.original_url, tl.source
ORDER BY clicks_24h DESC;
```

## 🚀 Implementation Requirements

### 1. Short URL Generation

- **Encoding**: Base62 (A-Z, a-z, 0-9)
- **Length**: 6-8 characters
- **Uniqueness**: Ensure no collisions
- **Generation**: Random + collision check

### 2. UTM Parameter Handling

- **Preserve Existing**: Don't overwrite existing query parameters
- **Merge Logic**: Append UTM params with `&` separator
- **Example**: `https://site.com/page?existing=1&utm_source=x&utm_medium=social`

### 3. Session Tracking

- **Cookie Name**: `em_session`
- **Generation**: UUID v4 or fallback to random string
- **Storage**: localStorage with fallback
- **Lifetime**: Persistent until cleared

### 4. Error Handling

- **Invalid Short Code**: 404 with friendly message
- **Domain Mismatch**: 400 with explanation
- **Rate Limit Exceeded**: 429 with retry-after
- **Invalid Site**: 400 with domain validation error

## 🧪 Testing Requirements

### Unit Tests

- Source detection logic
- UTM parameter merging
- Short code generation
- Database operations

### Integration Tests

- End-to-end link creation and tracking
- Click recording and analytics
- Pageview ingestion
- Dashboard data aggregation

### Manual Tests

- Create site and copy snippet
- Create tracked link and get short URL
- Visit short URL and verify redirect
- Verify analytics in dashboard
- Test source detection with/without UTMs

## 📱 UI/UX Requirements

### Dashboard Layout

- **Sites Page**: List sites with add/edit/delete + snippet copy
- **Links Page**: List links with add/edit/delete + URL copy
- **Overview Page**: 24h traffic chart + summary cards

### Mobile Responsiveness

- **DaisyUI Components**: Use responsive grid and components
- **Touch Friendly**: Adequate button sizes and spacing
- **Readable Charts**: Ensure charts work on small screens

### User Experience

- **Copy Buttons**: One-click copying of snippets and URLs
- **Empty States**: Helpful guidance when no data exists
- **Loading States**: Show progress for async operations
- **Error Handling**: Clear error messages and recovery steps

## 🚀 Deployment Considerations

### Environment Variables

```bash
DATABASE_URL=sqlite:///./engagemeter.db
SECRET_KEY=your-secret-key-here
ENVIRONMENT=production
RATE_LIMIT_REDIRECT=100
RATE_LIMIT_INGEST=1000
```

### Production Requirements

- **HTTPS**: Required for production
- **Database**: Consider PostgreSQL for scale
- **Caching**: Redis for rate limiting and session storage
- **Monitoring**: Health checks and error tracking
- **Backup**: Regular database backups

### Performance Targets

- **Page Load**: < 2 seconds
- **API Response**: < 500ms
- **Concurrent Users**: 100+ simultaneous
- **Data Retention**: 90 days for events

---

**Next Steps**: Implement database migrations, create models, and build the core tracking functionality.
