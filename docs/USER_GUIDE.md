# 👥 User Guide - EngageMeter

> **Complete guide to using EngageMeter Social Media Analytics effectively**

## 🎯 Getting Started

Welcome to EngageMeter! This guide will help you get the most out of your social media engagement analytics.

### What You'll Learn

- How to create and manage your account
- How to upload and analyze your social media data
- How to configure engagement scoring for your strategy
- How to interpret your dashboard and insights
- Best practices for optimizing your social media performance

## 🔐 Account Management

### Creating Your Account

1. **Navigate to EngageMeter** at your local installation or deployed URL
2. **Click "Get Started"** on the landing page
3. **Choose "Register"** to create a new account
4. **Fill in your details**:
   - Email address (will be used for login)
   - Username (unique identifier)
   - Password (minimum 8 characters)
5. **Click "Create Account"**

### Logging In

1. **Go to the login page**
2. **Enter your email and password**
3. **Click "Sign In"**
4. **You'll be redirected to your dashboard**

### Managing Your Profile

- **View Profile**: Click your username in the navigation bar
- **Change Password**: Available in profile settings
- **Account Settings**: Manage your preferences and data

## 📊 Data Import

### Understanding CSV Formats

EngageMeter supports multiple CSV formats from various social media platforms:

#### X Analytics (Twitter) Format

**Tweet-Level Data** (Individual posts):

```csv
Tweet ID,Tweet text,Posted date,Likes,Retweets,Replies,Mentions
123456,Great content!,2024-01-15,150,25,12,3
123457,Another post,2024-01-16,89,15,8,1
```

**Account Overview Data** (Daily summaries):

```csv
Date,Impressions,Likes,Engagements,Bookmarks,Shares,New follows,Unfollows,Replies,Reposts,Profile visits
2024-01-15,5866,9,88,5,0,0,0,5,0,35
2024-01-16,48,0,3,0,0,2,1,0,0,0
```

#### Other Platform Formats

EngageMeter automatically detects column names and maps them to the appropriate fields. Common variations include:

- **Likes**: "Likes", "likes", "Like count", "like_count"
- **Retweets**: "Retweets", "retweets", "Reposts", "retweet_count"
- **Replies**: "Replies", "replies", "Reply count", "reply_count"
- **Mentions**: "Mentions", "mentions", "Mention count", "mention_count"

### Uploading Your Data

1. **Navigate to Upload** in the main navigation
2. **Choose your CSV file** from your device
3. **Click "Upload & Process"**
4. **Wait for processing** (usually takes a few seconds)
5. **Review the results**:
   - Records processed
   - Records stored
   - Any errors encountered

### Upload Best Practices

- **File Size**: Keep files under 10MB for optimal performance
- **Data Quality**: Ensure your CSV has clean, consistent data
- **Regular Updates**: Upload new data weekly or monthly for ongoing insights
- **Backup**: Keep original CSV files as backups

## 🎯 Engagement Scoring

### Understanding the Scoring System

EngageMeter uses a configurable point system to calculate engagement scores:

**Formula**: `(Likes × Like Points) + (Retweets × Retweet Points) + (Replies × Reply Points) + (Mentions × Mention Points)`

### Default Point Values

- **Likes**: 1 point
- **Retweets**: 2 points
- **Replies**: 3 points
- **Mentions**: 1 point

### Customizing Your Scoring

1. **Go to Settings** in the navigation
2. **View Current Point Values** section
3. **Adjust the numbers** based on your strategy:
   - Higher points for actions you want to encourage
   - Lower points for less important metrics
4. **Click "Update Point Values"**
5. **All scores recalculate automatically**

### Scoring Strategy Examples

#### **Engagement-Focused Strategy**

- Likes: 1 point
- Retweets: 3 points (encourage sharing)
- Replies: 5 points (encourage conversation)
- Mentions: 2 points (encourage brand mentions)

#### **Reach-Focused Strategy**

- Likes: 1 point
- Retweets: 4 points (maximize reach)
- Replies: 2 points
- Mentions: 1 point

#### **Community-Building Strategy**

- Likes: 1 point
- Retweets: 2 points
- Replies: 6 points (encourage discussion)
- Mentions: 3 points (encourage community interaction)

## 📈 Dashboard Analytics

### Understanding Your Dashboard

The dashboard provides comprehensive insights into your social media performance:

#### **Key Metrics Overview**

- **Total Score**: Sum of all engagement scores
- **Total Posts**: Number of posts analyzed
- **Average Score**: Mean engagement score per post
- **Top Score**: Highest individual post score

#### **Engagement Breakdown**

Visual representation of how your engagement is distributed:

- **Likes**: Percentage of total engagement from likes
- **Retweets**: Percentage from retweets
- **Replies**: Percentage from replies
- **Mentions**: Percentage from mentions

#### **Top Performing Content**

- **Sort by Score**: See your best-performing posts
- **Filter by Date**: Analyze performance over time
- **Export Data**: Download insights for external analysis

### Using Dashboard Features

#### **Sorting and Filtering**

1. **Click column headers** to sort by different metrics
2. **Use score range filters** to focus on specific performance levels
3. **Limit results** to see top performers
4. **Search and filter** by date ranges

#### **Real-Time Updates**

- **HTMX integration** provides instant feedback
- **No page refreshes** needed for most actions
- **Live score calculations** when you change point values

## ⚙️ Settings and Configuration

### Point Value Management

#### **Updating Point Values**

1. **Navigate to Settings**
2. **View current configuration**
3. **Enter new values** in the form
4. **Click "Update Point Values"**
5. **See immediate impact** on all scores

#### **Strategy Impact Analysis**

The settings page shows:

- **Current scoring formula** with actual values
- **Example scenarios** (high/medium/low engagement)
- **Strategy recommendations** based on your configuration
- **Performance insights** for optimization

### Account Preferences

- **Session management** for security
- **Data retention** policies
- **Export preferences** for data downloads

## 📱 Mobile Experience

### Responsive Design Features

- **Touch-friendly interface** for mobile devices
- **Optimized layouts** for small screens
- **Fast loading** on mobile networks
- **Offline capabilities** for basic functionality

### Mobile Best Practices

- **Use landscape mode** for better data viewing
- **Pinch to zoom** for detailed analysis
- **Swipe gestures** for navigation
- **Save to home screen** for quick access

## 🔍 Data Analysis

### Understanding Your Metrics

#### **Engagement Score Interpretation**

- **0-10**: Low engagement, consider content strategy
- **11-25**: Moderate engagement, room for improvement
- **26-50**: Good engagement, content is resonating
- **51+**: Excellent engagement, content is highly effective

#### **Trend Analysis**

- **Weekly patterns**: Identify best posting times
- **Content types**: See what resonates with your audience
- **Seasonal trends**: Understand temporal patterns
- **Growth trajectory**: Track improvement over time

### Performance Insights

#### **Content Optimization**

- **High-scoring posts**: Analyze what works
- **Low-scoring posts**: Identify improvement areas
- **Engagement patterns**: Understand audience preferences
- **Timing insights**: Find optimal posting schedules

#### **Strategy Recommendations**

- **Point value adjustments** based on goals
- **Content focus** recommendations
- **Posting frequency** suggestions
- **Audience engagement** strategies

## 🚀 Advanced Features

### CSV Format Detection

EngageMeter automatically:

- **Detects CSV format** (tweet-level vs. account overview)
- **Maps column names** to appropriate fields
- **Handles data variations** from different platforms
- **Creates synthetic records** for daily summaries

### Score Recalculation

When you update point values:

- **All scores recalculate** automatically
- **Historical data** maintains consistency
- **Performance impact** is immediate
- **Data integrity** is preserved

### Export and Integration

- **Download processed data** for external analysis
- **API endpoints** for custom integrations
- **Data portability** for platform migration
- **Backup capabilities** for data safety

## 🎯 Best Practices

### Content Strategy

1. **Analyze top performers** to understand what works
2. **Test different content types** and measure results
3. **Optimize posting times** based on engagement data
4. **Engage with your audience** to boost interaction

### Data Management

1. **Upload data regularly** for ongoing insights
2. **Keep historical data** for trend analysis
3. **Validate CSV format** before uploading
4. **Backup your data** regularly

### Performance Optimization

1. **Set realistic point values** based on your goals
2. **Focus on high-impact metrics** for your strategy
3. **Monitor trends** over time, not just individual posts
4. **Iterate and improve** based on data insights

## 🚨 Troubleshooting

### Common Issues

#### **Upload Problems**

- **File format**: Ensure CSV format is correct
- **Column names**: Check that required columns are present
- **File size**: Keep files under 10MB
- **Encoding**: Use UTF-8 encoding for special characters

#### **Scoring Issues**

- **Point values**: Verify point values are positive numbers
- **Data quality**: Check for missing or invalid data
- **Recalculation**: Ensure scores update after point value changes

#### **Dashboard Problems**

- **Browser compatibility**: Use modern browsers (Chrome, Firefox, Safari, Edge)
- **JavaScript**: Ensure JavaScript is enabled
- **Cache**: Clear browser cache if issues persist

### Getting Help

- **Check the logs** for error messages
- **Review documentation** for solutions
- **Contact support** for persistent issues
- **Community forums** for peer assistance

## 🔮 Future Features

### Upcoming Enhancements

- **Multi-platform support** for Instagram, LinkedIn, TikTok
- **Advanced analytics** with machine learning insights
- **Team collaboration** features for agencies
- **API integrations** with popular social media tools
- **Mobile app** for on-the-go analytics

### Feature Requests

- **Submit ideas** through GitHub issues
- **Vote on features** in community discussions
- **Contribute code** for open source development
- **Share feedback** to improve the platform

## 📚 Additional Resources

### Learning Materials

- **Video tutorials** for visual learners
- **Case studies** of successful strategies
- **Webinar recordings** with expert insights
- **Community discussions** for peer learning

### Support Channels

- **Documentation**: Comprehensive guides and references
- **GitHub Issues**: Bug reports and feature requests
- **Community Forum**: Peer support and discussions
- **Email Support**: Direct assistance for complex issues

---

**🎯 You're now ready to master EngageMeter and optimize your social media engagement strategy!**

For additional help, check the [API Reference](API_REFERENCE.md) or [Deployment Guide](DEPLOYMENT.md).
