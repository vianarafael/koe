# 🎯 EngageMeter.co Development Tickets

## 📊 Project Status

**PRODUCT PIVOT**: From Social Media Analytics to Simple Funnel Tracking

**Previous Focus**: Social media engagement analytics with CSV imports  
**New Focus**: Simple analytics for indie hackers tracking X → website → monetization  
**Status**: Pivot Defined, Ready for MVP Development

## 🚀 **NEW MVP ROADMAP: Simple Funnel Tracker**

### **EPIC 1: Core Infrastructure & Data Models**

- **T01**: User authentication system (email/password) - **COMPLETED ✅**
- **T02**: Database schema and migrations for sites, tracked_links, events - **IN PROGRESS 🔄**
- **T03**: Site management models and CRUD operations
- **T04**: Link tracking models and database operations
- **T05**: Event tracking models and analytics foundation

### **EPIC 2: Link Generation & Tracking**

- **T06**: Short URL generation with base62 encoding
- **T07**: UTM parameter handling and query string preservation
- **T08**: Redirect endpoint with click tracking
- **T09**: Domain validation and security measures
- **T10**: Rate limiting implementation

### **EPIC 3: JavaScript Snippet & Ingestion**

- **T11**: JS tracking snippet with privacy-first design
- **T12**: Pageview ingestion endpoint (`/v1/ingest`)
- **T13**: Source detection logic (UTM + referrer mapping)
- **T14**: Session tracking and cookie management

### **EPIC 4: Dashboard & Analytics**

- **T15**: Site management UI (add/edit/delete sites)
- **T16**: Link management UI (add/edit/delete links)
- **T17**: 24h traffic visualization with bar charts
- **T18**: Analytics aggregation and real-time updates
- **T19**: Copy buttons and user experience polish

### **EPIC 5: Production & Testing**

- **T20**: Comprehensive test suite
- **T21**: Production deployment and monitoring
- **T22**: Documentation updates and user guides
- **T23**: Performance optimization and final polish

## 🎯 **MVP Success Criteria**

### **Must Have ✅**

1. **User can register/login** with email/password
2. **User can add multiple sites** (domains) to track
3. **User can add website URLs** to track per site
4. **System generates short URLs** with UTM parameters
5. **JS snippet tracks visits** to user's site (privacy-first)
6. **Dashboard shows 24h traffic** by source with bar chart
7. **User can manage** (add/edit/delete) tracked links
8. **Source detection works** with and without UTMs

### **Nice to Have 🎨**

1. **Simple traffic graphs** (24h by hour)
2. **Click count per link**
3. **Basic user settings**
4. **Mobile-responsive design**
5. **Copy buttons** for snippets and URLs

## 📋 **Technical Requirements**

### **Backend (Keep)**

- [x] FastAPI framework
- [x] SQLite database
- [x] User authentication
- [x] Session management

### **Backend (Add)**

- [ ] **Site management models** (sites table)
- [ ] **Link tracking models** (tracked_links table)
- [ ] **Event tracking models** (events table)
- [ ] **Short URL generation** (base62 encoding)
- [ ] **Click ingestion API** (`/v1/ingest`)
- [ ] **Redirect handling** (`/{short_code}`)
- [ ] **Traffic aggregation** (24h by source)
- [ ] **Rate limiting** (leaky bucket)
- [ ] **Domain validation** (prevent open redirects)

### **Frontend (Keep)**

- [x] HTMX for interactions
- [x] DaisyUI components
- [x] Responsive design
- [x] User dashboard structure

### **Frontend (Add)**

- [ ] **Site management forms** (add/edit/delete sites)
- [ ] **Link management forms** (add/edit/delete links)
- [ ] **Traffic visualization** (24h bar charts)
- [ ] **Copy buttons** for snippets and URLs
- [ ] **Empty states** and user guidance

## 🔄 **Migration Plan**

### **Phase 1: Remove Old Features**

- [ ] Remove CSV upload functionality
- [ ] Remove engagement scoring
- [ ] Remove social media analytics
- [ ] Clean up old database tables
- [ ] Update navigation and UI

### **Phase 2: Build New Core**

- [ ] Create site management models and UI
- [ ] Create link tracking models and database schema
- [ ] Build short URL generation with UTM support
- [ ] Implement JS tracking snippet
- [ ] Create simple dashboard with 24h charts
- [ ] Add link management UI

### **Phase 3: Polish & Deploy**

- [ ] UI/UX improvements
- [ ] Testing and bug fixes
- [ ] Production deployment
- [ ] Documentation updates

## 🚫 **OUT OF SCOPE (Not MVP)**

### **CSV Import & Social Analytics**

- [x] ~~CSV parsing and X Analytics support~~ (Remove)
- [x] ~~Engagement scoring engine~~ (Remove)
- [x] ~~Social media performance metrics~~ (Remove)
- [x] ~~Goal setting and progress tracking~~ (Remove)
- [x] ~~Best time to post analysis~~ (Remove)

### **Advanced Analytics**

- [x] ~~Complex filtering and date ranges~~ (Remove)
- [x] ~~Engagement breakdowns~~ (Remove)
- [x] ~~Performance optimization suggestions~~ (Remove)
- [x] ~~Export functionality~~ (Remove)

### **Complex Features**

- [x] ~~Multiple user roles~~ (Remove)
- [x] ~~Team collaboration~~ (Remove)
- [x] ~~API integrations~~ (Remove)
- [x] ~~Webhook support~~ (Remove)

## 🎯 **Why This Scope?**

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

## 📊 **Current Development Status**

### **Completed ✅**

- **T01**: User authentication system (email/password)
- **T02**: User registration and login
- **T03**: Session management
- **T04**: Protected routes and middleware
- **T05**: Database schema for users
- **T06**: Frontend templates with authentication
- **T07**: Comprehensive test suite

### **In Progress 🔄**

- **T08**: Database schema and migrations for new models
- **T09**: Site management models and operations
- **T10**: Link tracking models and database operations

### **Next Up 🎯**

- **T11**: Short URL generation system
- **T12**: JS tracking snippet implementation
- **T13**: Redirect endpoint with click tracking
- **T14**: Pageview ingestion API
- **T15**: Site management UI
- **T16**: Link management UI
- **T17**: 24h traffic visualization

---

**Total Points**: 23 (New MVP)  
**Completed**: 9  
**Remaining**: 14  
**Completion**: 39%

## 🚀 **Implementation Priority**

### **Week 1: Core Infrastructure**

- Database migrations and models
- Site and link management
- Basic CRUD operations

### **Week 2: Tracking & Analytics**

- Short URL generation
- Click tracking and redirects
- Pageview ingestion

### **Week 3: Dashboard & Polish**

- Analytics dashboard
- Traffic visualization
- UI/UX improvements

### **Week 4: Testing & Deployment**

- Comprehensive testing
- Production deployment
- Documentation updates
