from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional, List
from datetime import datetime, timedelta
from app.auth import get_current_user
from app.models import User, UserGoal, GoalProgress, CreateGoalRequest, GoalResponse, GoalTemplate
from app.db import get_db, create_user_goal, get_user_goals, get_user_goal, update_goal_progress, delete_user_goal
from app.templates import get_templates

router = APIRouter(prefix="/goals", tags=["goals"])
templates = get_templates()

# Goal Templates Configuration
GOAL_TEMPLATES = {
    "grow_impressions": {
        "id": "grow_impressions",
        "name": "📈 Grow Impressions",
        "description": "Reach more people with your posts.",
        "category": "growth",
        "primary_metric": "impressions",
        "secondary_metrics": [],
        "default_targets": {
            "starter": {"value": 100000, "unit": "impressions", "timeframe": 30},
            "intermediate": {"value": 500000, "unit": "impressions", "timeframe": 30},
            "advanced": {"value": 1000000, "unit": "impressions", "timeframe": 30}
        },
        "coaching_tips": [
            "Post consistently - aim for 1-3 tweets per day",
            "Use trending hashtags to increase discoverability",
            "Engage with other users' content to boost visibility"
        ]
    },
    "grow_followers": {
        "id": "grow_followers",
        "name": "👥 Grow Followers",
        "description": "Turn readers into community.",
        "category": "growth",
        "primary_metric": "followers",
        "secondary_metrics": [],
        "default_targets": {
            "starter": {"value": 100, "unit": "followers", "timeframe": 30},
            "intermediate": {"value": 500, "unit": "followers", "timeframe": 30},
            "advanced": {"value": 1000, "unit": "followers", "timeframe": 30}
        },
        "coaching_tips": [
            "Reply to comments and engage with your audience",
            "Share valuable content that people want to save",
            "Collaborate with other creators in your niche"
        ]
    },
    "boost_engagement": {
        "id": "boost_engagement",
        "name": "💬 Boost Engagement",
        "description": "Get more replies, reposts, and conversations.",
        "category": "engagement",
        "primary_metric": "replies",
        "secondary_metrics": ["retweets", "likes"],
        "default_targets": {
            "starter": {"value": 50, "unit": "replies", "timeframe": 30},
            "intermediate": {"value": 200, "unit": "replies", "timeframe": 30},
            "advanced": {"value": 500, "unit": "replies", "timeframe": 30}
        },
        "coaching_tips": [
            "Ask questions to encourage responses",
            "Share personal stories that resonate",
            "Create content that sparks discussion"
        ]
    },
    "monetization_path": {
        "id": "monetization_path",
        "name": "💵 Monetization Path (recommended)",
        "description": "X requires 5M impressions in 3 months + 500 verified followers.",
        "category": "monetization",
        "primary_metric": "impressions",
        "secondary_metrics": ["followers"],
        "default_targets": {
            "primary": {"value": 5000000, "unit": "impressions", "timeframe": 90},
            "secondary": {"value": 500, "unit": "followers", "timeframe": 90}
        },
        "coaching_tips": [
            "Focus on high-engagement content to boost impressions",
            "Build authentic relationships to grow verified followers",
            "Post consistently - algorithm favors active accounts"
        ]
    }
}

@router.get("/", response_class=HTMLResponse)
async def goals_page(request: Request, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """Display goals page with template selection"""
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=302)
    
    # Get user's existing goals
    user_goals = await get_user_goals(db, current_user.id)
    
    template = templates.get_template("goals.html")
    return HTMLResponse(template.render(
        request=request,
        current_user=current_user,
        goal_templates=GOAL_TEMPLATES,
        user_goals=user_goals
    ))

@router.post("/create", response_class=HTMLResponse)
async def create_goal(
    request: Request,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
    goal_type: str = Form(...),
    target_value: int = Form(...),
    timeframe_days: int = Form(...),
    is_custom: bool = Form(False),
    custom_metric: Optional[str] = Form(None)
):
    """Create a new goal with coaching validation"""
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=302)
    
    # Calculate dates
    start_date = datetime.now()
    end_date = start_date + timedelta(days=timeframe_days)
    
    # Create goal
    goal = UserGoal(
        user_id=current_user.id,
        goal_type=goal_type,
        target_value=target_value,
        start_date=start_date,
        end_date=end_date,
        unit=custom_metric if is_custom else GOAL_TEMPLATES.get(goal_type, {}).get("primary_metric", "units"),
        is_primary=True
    )
    
    # Validate goal with coaching feedback
    coaching_feedback = validate_goal_with_coaching(goal, current_user)
    
    # Save goal
    created_goal = await create_user_goal(db, goal)
    
    # Redirect back to goals page with success message
    return RedirectResponse(url="/goals?success=true", status_code=302)

@router.post("/delete/{goal_id}")
async def delete_goal(
    goal_id: str,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db)
):
    """Delete a user goal"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Verify goal belongs to user
    goal = await get_user_goal(db, goal_id)
    if not goal or goal.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    await delete_user_goal(db, goal_id)
    return {"message": "Goal deleted successfully"}

def validate_goal_with_coaching(goal: UserGoal, user: User) -> str:
    """Provide coaching feedback on goal setting"""
    # This is a simplified version - in production, you'd analyze user's historical data
    
    if goal.goal_type == "monetization_path":
        if goal.target_value >= 5000000:
            return "Perfect! That's challenging but achievable for X monetization. Focus on consistent posting and high-engagement content."
        else:
            return "Consider aiming higher - X requires 5M impressions in 3 months for Creator Fund access."
    
    # For other goals, provide general coaching
    if goal.target_value < 100:
        return "That's a safe goal - consider stretching yourself a bit more for faster growth!"
    elif goal.target_value > 1000000:
        return "Ambitious! Make sure you have a solid content strategy and posting schedule to hit this target."
    else:
        return "Great goal! Challenging but achievable. You've got this! 🚀"
