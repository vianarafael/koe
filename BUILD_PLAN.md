# Build Plan

Build a minimal viable product for Koe that allows users to authenticate with Twitter, fetch their recent tweets and engagement metrics, assign point values to interaction types, and view a dashboard summarizing engagement scores. Focus on fast iteration with a lean stack and simple UI. Prioritize core flows and deploy within one week.

## 📝 Commit Plan

1. Commit 1: Setup project structure, dependencies, and initial FastAPI backend
2. Commit 2: Implement Twitter OAuth backend and frontend UI
3. Commit 3: Add tweet fetching and database storage logic
4. Commit 4: Implement engagement scoring logic and API endpoints
5. Commit 5: Build React dashboard UI to display engagement scores
6. Commit 6: Add user settings UI and backend for point values
7. Commit 7: Write automated tests for all key flows
8. Commit 8: Deploy MVP to public URL and verify end-to-end functionality

## 🧪 Test Plan

- **Test1**: OAuth flow test: simulate user login and verify token storage
- **Test2**: Data fetch test: mock Twitter API response and verify database update
- **Test3**: Scoring logic test: input sample engagement data and verify correct score output
- **Test4**: Dashboard render test: verify UI displays tweets with correct scores
- **Test5**: Settings update test: change point values and verify recalculated scores

