# 🎯 EngageMeter.co Development Tickets

## 📊 Project Status

**PRODUCT PIVOT**: From Social Media Analytics to Simple Funnel Tracking

**Previous Focus**: Social media engagement analytics with CSV imports  
**New Focus**: Simple analytics for indie hackers tracking X → website → monetization  
**Status**: Pivot Defined, Ready for MVP Development

## 🚀 **NEW MVP ROADMAP: Simple Funnel Tracker**

### **EPIC 1: Core Tracking Infrastructure**

- **T01**: User authentication system (email/password) - **COMPLETED ✅**
- **T02**: Link tracking models and database schema
- **T03**: Short URL generation with UTM parameters
- **T04**: JS tracking snippet for website integration

### **EPIC 2: Dashboard & Analytics**

- **T05**: Simple dashboard showing tracked links
- **T06**: 24h traffic visualization by source
- **T07**: Link management (add/edit/delete)
- **T08**: Basic traffic analytics and insights

### **EPIC 3: Production & Polish**

- **T09**: JS snippet serving and optimization
- **T10**: Click ingestion and data aggregation
- **T11**: Production deployment and monitoring
- **T12**: UI/UX polish and mobile optimization

## 🎯 **MVP Success Criteria**

### **Must Have ✅**

1. **User can register/login** with email/password
2. **User can add website URLs** to track
3. **System generates short URLs** with UTM parameters
4. **JS snippet tracks visits** to user's site
5. **Dashboard shows 24h traffic** by source
6. **User can manage** (add/edit/delete) tracked links

### **Nice to Have 🎨**

1. **Simple traffic graphs**
2. **Click count per link**
3. **Basic user settings**
4. **Mobile-responsive design**

## 📋 **Technical Requirements**

### **Backend (Keep)**

- [x] FastAPI framework
- [x] SQLite database
- [x] User authentication
- [x] Session management

### **Backend (Add)**

- [ ] Link tracking models
- [ ] Short URL generation
- [ ] Click ingestion API
- [ ] Traffic aggregation

### **Frontend (Keep)**

- [x] HTMX for interactions
- [x] DaisyUI components
- [x] Responsive design
- [x] User dashboard structure

### **Frontend (Add)**

- [ ] Link management forms
- [ ] Traffic visualization
- [ ] Simple analytics display

## 🔄 **Migration Plan**

### **Phase 1: Remove Old Features**

- [ ] Remove CSV upload functionality
- [ ] Remove engagement scoring
- [ ] Remove social media analytics
- [ ] Clean up old database tables
- [ ] Update navigation and UI

### **Phase 2: Build New Core**

- [ ] Create link tracking models
- [ ] Build short URL generation
- [ ] Implement JS tracking snippet
- [ ] Create simple dashboard
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

- **T08**: Link tracking models and database schema
- **T09**: Short URL generation system
- **T10**: JS tracking snippet implementation

### **Next Up 🎯**

- **T11**: Simple dashboard for tracked links
- **T12**: Traffic visualization and analytics
- **T13**: Link management UI
- **T14**: Production deployment

---

**Total Points**: 14 (New MVP)  
**Completed**: 7  
**Remaining**: 7  
**Completion**: 50%
