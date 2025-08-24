# Dashboard Design UI Mockups

## 📊 Overview

The dashboard is the central hub for users to view their engagement analytics, track performance trends, and analyze their social media content effectiveness. The design emphasizes data clarity, interactive exploration, and actionable insights.

## 🎯 Page Layout

### **Main Dashboard (Authenticated)**

```
┌─────────────────────────────────────────────────────────────┐
│ Koe  [Dashboard] [Upload] [Settings] [Profile ▼] [Logout] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Welcome back, username!                                    │
│  Here's your engagement overview                            │
│                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │ Total Score │ │ Total Posts │ │ Avg Score   │ │ Top     │ │
│  │    1,247   │ │     45      │ │   27.7      │ │ Score   │ │
│  │   +12%     │ │   +3 today  │ │   +2.1      │ │   89    │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
│                                                             │
│  Engagement Breakdown                                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │    Likes    │ │  Retweets   │ │   Replies   │ │Mentions │ │
│  │    45%      │ │    25%      │ │    20%      │ │  10%    │ │
│  │   [Chart]   │ │   [Chart]   │ │   [Chart]   │ │ [Chart] │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
│                                                             │
│  Top Performing Tweets                                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Score │ Date      │ Tweet Preview           │ Engagement │ │
│  │ ──────┼ ─────────┼ ───────────────────────┼ ────────── │ │
│  │  89   │ Aug 24   │ "Just launched our new…"│ 45❤️ 12🔄 │ │
│  │  76   │ Aug 23   │ "Excited to share..."   │ 32❤️ 8🔄  │ │
│  │  67   │ Aug 22   │ "Big announcement..."   │ 28❤️ 6🔄  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  Recent Activity                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ [Upload CSV] [View All Tweets] [Export Data]           │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key Sections:**

- Welcome message with user personalization
- Key metrics overview cards
- Engagement breakdown visualization
- Top performing tweets table
- Quick action buttons

## 📈 Metrics Cards

### **Score Overview Cards**

```
┌─────────────────────────────────────────────────────────────┐
│ Total Score                                                 │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │                                                         │ │
│ │                   1,247                                 │ │
│ │                   +12% from last week                   │ │
│ │                                                         │ │
│ │  [📈 View Trend]                                       │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Card States:**

- **Positive Change**: Green text, upward arrow
- **Negative Change**: Red text, downward arrow
- **No Change**: Gray text, horizontal line
- **Loading**: Skeleton animation
- **Hover**: Subtle shadow and scale effect

### **Engagement Breakdown Cards**

```
┌─────────────────────────────────────────────────────────────┐
│ Likes                                                      │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │                                                         │ │
│ │                   45%                                   │ │
│ │                                                         │ │
│ │  ┌─────────────────────────────────────────────────────┐ │
│ │  │ ████████████████████████████████████████████████████ │ │
│ │  └─────────────────────────────────────────────────────┘ │
│ │                                                         │ │
│ │  Total: 234 likes                                       │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Visual Elements:**

- Percentage display prominently
- Progress bar visualization
- Total count below
- Color coding by engagement type
- Interactive hover states

## 📊 Data Tables

### **Tweets Table with Sorting**

```
┌─────────────────────────────────────────────────────────────┐
│ Filters & Sorting                                           │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Sort by: [Score ▼] [Date] [Engagement] [Likes]        │ │
│ │ Order: [Descending ▼] [Ascending]                      │ │
│ │ Score Range: [Min: 0] [Max: 100] [Apply]              │ │
│ │ Results: [Show 25 ▼] [50] [100]                        │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  Tweets Table                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Score │ Date      │ Tweet Text           │ Engagement  │ │
│  │ ──────┼ ─────────┼ ─────────────────────┼ ─────────── │ │
│  │  89   │ Aug 24   │ "Just launched our…" │ 45❤️ 12🔄   │ │
│  │       │ 14:30    │ [View Full Tweet]    │ 8💬 3@      │ │
│  │ ──────┼ ─────────┼ ─────────────────────┼ ─────────── │ │
│  │  76   │ Aug 23   │ "Excited to share..."│ 32❤️ 8🔄    │ │
│  │       │ 09:15    │ [View Full Tweet]    │ 5💬 2@      │ │
│  │ ──────┼ ─────────┼ ─────────────────────┼ ─────────── │ │
│  │  67   │ Aug 22   │ "Big announcement..."│ 28❤️ 6🔄    │ │
│  │       │ 16:45    │ [View Full Tweet]    │ 4💬 1@      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  Showing 1-25 of 45 results                                │
│  [← Previous] [1] [2] [Next →]                            │
└─────────────────────────────────────────────────────────────┘
```

**Table Features:**

- Sortable columns with visual indicators
- Expandable rows for full tweet content
- Pagination controls
- Filter options for score ranges
- Result count display

### **Score Visualization**

```
┌─────────────────────────────────────────────────────────────┐
│ Score Distribution                                          │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │                                                         │ │
│ │  High (80-100): ████████ 8 posts                       │ │
│ │  Good (60-79):  ████████████ 12 posts                  │ │
│ │  Fair (40-59):  ████████ 8 posts                       │ │
│ │  Low (20-39):   █████ 5 posts                          │ │
│ │  Poor (0-19):   ██ 2 posts                             │ │
│ │                                                         │ │
│ │  [View Detailed Breakdown]                              │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🔍 Interactive Elements

### **Sorting Controls**

```
┌─────────────────────────────────────────────────────────────┐
│ Sort by: [Score ▼]                                         │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Score ▼ (High to Low)                                   │ │
│ │ Date (Newest First)                                     │ │
│ │ Engagement (Total Count)                                 │ │
│ │ Likes (Count)                                            │ │
│ │ Retweets (Count)                                         │ │
│ │ Replies (Count)                                          │ │
│ │ Mentions (Count)                                         │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Sorting States:**

- **Active**: Blue background, white text
- **Inactive**: Gray background, dark text
- **Direction**: Arrow indicators (↑↓)
- **Hover**: Subtle background change

### **Filter Controls**

```
┌─────────────────────────────────────────────────────────────┐
│ Score Range Filter                                          │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Min Score: [0] ────────────────── [100] Max Score      │ │
│ │                                                         │ │
│ │ [Apply Filters] [Clear All]                             │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Filter Features:**

- Range slider for score selection
- Input fields for precise values
- Apply/Clear buttons
- Real-time result count updates
- Visual feedback for active filters

## 📱 Responsive Design

### **Mobile Layout (320px - 768px)**

```
┌─────────────────────────────────────────────────────────────┐
│ [☰] Koe                                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Welcome back, username!                                   │
│                                                             │
│  ┌─────────────┐                                           │
│  │ Total Score │                                           │
│  │    1,247   │                                           │
│  │   +12%     │                                           │
│  └─────────────┘                                           │
│                                                             │
│  ┌─────────────┐                                           │
│  │ Total Posts │                                           │
│  │     45      │                                           │
│  │   +3 today │                                           │
│  └─────────────┘                                           │
│                                                             │
│  [View All Metrics]                                        │
│                                                             │
│  Top Tweets                                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Score: 89                                               │
│  │ "Just launched our new..."                             │
│  │ 45❤️ 12🔄 8💬 3@                                        │
│  │ [View Details]                                          │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  [Upload CSV] [View All]                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Mobile Adaptations:**

- Single column layout
- Stacked metric cards
- Simplified navigation
- Touch-friendly buttons
- Swipe gestures for tables

### **Tablet Layout (768px - 1024px)**

- Two-column metric layout
- Side-by-side engagement breakdown
- Compact table with horizontal scroll
- Medium-sized touch targets

### **Desktop Layout (1024px+)**

- Four-column metric layout
- Full table with all columns visible
- Hover effects and animations
- Advanced filtering options

## 🎨 Visual Design

### **Color Scheme**

```
Primary Colors:
- Background: #FFFFFF (white)
- Surface: #F9FAFB (light gray)
- Border: #E5E7EB (medium gray)
- Text: #111827 (dark gray)

Accent Colors:
- Primary: #3B82F6 (blue)
- Success: #10B981 (green)
- Warning: #F59E0B (yellow)
- Error: #EF4444 (red)

Score Colors:
- High (80-100): #10B981 (green)
- Good (60-79): #3B82F6 (blue)
- Fair (40-59): #F59E0B (yellow)
- Low (20-39): #F97316 (orange)
- Poor (0-19): #EF4444 (red)
```

### **Typography Hierarchy**

```
Page Title: text-3xl font-bold text-gray-900
Section Headers: text-xl font-semibold text-gray-800
Card Titles: text-lg font-medium text-gray-700
Metric Values: text-2xl font-bold text-gray-900
Body Text: text-base text-gray-600
Small Text: text-sm text-gray-500
```

### **Spacing System**

```
Container Padding: 24px (1.5rem)
Section Margins: 32px (2rem)
Card Padding: 20px (1.25rem)
Element Spacing: 16px (1rem)
Compact Spacing: 8px (0.5rem)
```

## ♿ Accessibility Features

### **Screen Reader Support**

- Proper table headers and row associations
- ARIA labels for interactive elements
- Status announcements for data updates
- Navigation landmarks for page sections

### **Keyboard Navigation**

- Tab order follows logical flow
- Enter key expands/collapses rows
- Arrow keys navigate table cells
- Escape key closes modals and dropdowns

### **Visual Accessibility**

- High contrast color combinations
- Clear focus indicators
- Consistent visual hierarchy
- Readable font sizes and spacing

## 🚀 Performance Considerations

### **Loading States**

- Skeleton screens for initial load
- Progressive loading of data
- Lazy loading for large tables
- Optimistic updates for user actions

### **Data Management**

- Efficient pagination
- Smart caching strategies
- Debounced search and filters
- Optimized API calls

## 🎯 Success Metrics

### **User Engagement Goals**

- **Dashboard Visits**: >80% of users visit daily
- **Data Exploration**: >60% use sorting/filtering features
- **Export Usage**: >40% export data for analysis
- **Session Duration**: Average >10 minutes per visit

### **Performance Targets**

- **Page Load Time**: <2 seconds for dashboard
- **Data Updates**: <1 second for real-time changes
- **Table Rendering**: <500ms for 100+ rows
- **Mobile Performance**: <3 seconds on 3G connections

---

**Design Status**: Ready for Implementation  
**Review Required**: Product Owner, UX Designer  
**Next Phase**: Frontend Development
