# 🎯 EngageMeter.co - Feature Scope

This document defines what's **IN SCOPE** and **OUT OF SCOPE** for the EngageMeter.co MVP.

## 🚀 MVP Goal

**Super-simple analytics for indie hackers** who want to track X → website → monetization funnels.

## ✅ IN SCOPE (MVP Features)

### 🔧 Core Setup
- [x] **User Authentication**: Email/password registration and login
- [x] **Session Management**: Secure user sessions
- [ ] **JS Tracking Snippet**: One-line website integration (`<script src="...">`)

### 🔗 Link Tracking
- [ ] **URL Management**: Add, edit, delete website URLs to track
- [ ] **Source Selection**: Pick traffic source (X, Reddit, LinkedIn, Other)
- [ ] **Short URL Generation**: Auto-create minified links (e.g., `engmtr.co/abc123`)
- [ ] **UTM Parameters**: Automatic UTM tagging for source tracking

### 📊 Analytics Dashboard
- [ ] **24h Traffic View**: Bar graph of visits in last 24 hours
- [ ] **Source Breakdown**: Traffic by X, Reddit, LinkedIn, Other
- [ ] **Link Performance**: Show clicks per tracked URL
- [ ] **Simple Metrics**: Focus on traffic volume, not complex analytics

### 🚀 Management
- [ ] **Link CRUD**: Create, read, update, delete tracking URLs
- [ ] **Regenerate Links**: Delete and recreate short URLs as needed
- [ ] **User Dashboard**: Simple overview of all tracked links

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
1. **User can register/login**
2. **User can add website URLs to track**
3. **System generates short URLs with UTMs**
4. **JS snippet tracks visits to user's site**
5. **Dashboard shows 24h traffic by source**
6. **User can manage (add/edit/delete) tracked links**

### Nice to Have 🎨
1. **Simple traffic graphs**
2. **Click count per link**
3. **Basic user settings**
4. **Mobile-responsive design**

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
- [ ] Create link tracking models
- [ ] Build short URL generation
- [ ] Implement JS tracking snippet
- [ ] Create simple dashboard
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
- [ ] Link tracking models
- [ ] Short URL generation
- [ ] Click ingestion API
- [ ] Traffic aggregation

### Frontend (Keep)
- [x] HTMX for interactions
- [x] DaisyUI components
- [x] Responsive design
- [x] User dashboard structure

### Frontend (Add)
- [ ] Link management forms
- [ ] Traffic visualization
- [ ] Simple analytics display

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
