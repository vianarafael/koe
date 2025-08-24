from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from typing import Dict, Any
from app.auth import get_current_user
from app.models import User, SetPointValuesRequest, PointValuesResponse
from app.db import get_db, update_user_point_values, get_user_by_id
from app.scoring import scoring_engine
from app.templates import get_templates

router = APIRouter(prefix="/settings", tags=["settings"])
templates = get_templates()

@router.get("/", response_class=HTMLResponse)
async def settings_page(
    request: Request, 
    current_user: User = Depends(get_current_user),
    db=Depends(get_db)
):
    """Display user settings page for updating point values"""
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=302)
    
    # Get current point values
    current_points = current_user.point_values
    
    # Calculate sample impact for current strategy
    sample_impact = {
        "high_engagement": {
            "likes": 100, "retweets": 50, "replies": 25, "mentions": 10,
            "score": (100 * current_points["like"] + 50 * current_points["retweet"] + 
                     25 * current_points["reply"] + 10 * current_points["mention"])
        },
        "medium_engagement": {
            "likes": 50, "retweets": 25, "replies": 10, "mentions": 5,
            "score": (50 * current_points["like"] + 25 * current_points["retweet"] + 
                     10 * current_points["reply"] + 5 * current_points["mention"])
        },
        "low_engagement": {
            "likes": 10, "retweets": 5, "replies": 2, "mentions": 1,
            "score": (10 * current_points["like"] + 5 * current_points["retweet"] + 
                     2 * current_points["reply"] + 1 * current_points["mention"])
        }
    }
    
    template = templates.get_template("settings.html")
    return HTMLResponse(template.render(
        request=request,
        current_user=current_user,
        current_points=current_points,
        sample_impact=sample_impact
    ))

@router.post("/update-points", response_class=JSONResponse)
async def update_point_values(
    request: Request,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
    like: int = Form(...),
    retweet: int = Form(...),
    reply: int = Form(...),
    mention: int = Form(...)
):
    """Update user point values and recalculate all engagement scores"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        # Validate point values
        new_point_values = {
            "like": like,
            "retweet": retweet,
            "reply": reply,
            "mention": mention
        }
        
        # Validate using scoring engine
        if not scoring_engine.validate_point_values(new_point_values):
            raise HTTPException(status_code=400, detail="Invalid point values. All values must be non-negative integers.")
        
        # Update user's point values in database
        await update_user_point_values(db, current_user.id, new_point_values)
        
        # Recalculate all engagement scores for this user
        recalculated_count = await scoring_engine.recalculate_user_scores(
            current_user.id, 
            new_point_values, 
            db
        )
        
        # Get updated user data
        updated_user = await get_user_by_id(db, current_user.id)
        
        return {
            "success": True,
            "message": f"Point values updated successfully! {recalculated_count} engagement scores recalculated.",
            "updated_point_values": new_point_values,
            "recalculated_count": recalculated_count,
            "user_id": current_user.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating point values: {e}")
        raise HTTPException(status_code=500, detail="Error updating point values")

@router.post("/update-points-htmx", response_class=HTMLResponse)
async def update_point_values_htmx(
    request: Request,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
    like: int = Form(...),
    retweet: int = Form(...),
    reply: int = Form(...),
    mention: int = Form(...)
):
    """HTMX endpoint for updating point values with immediate UI feedback"""
    if not current_user:
        return HTMLResponse(
            '<div class="text-red-600">Authentication required</div>',
            status_code=401
        )
    
    try:
        # Validate point values
        new_point_values = {
            "like": like,
            "retweet": retweet,
            "reply": reply,
            "mention": mention
        }
        
        # Validate using scoring engine
        if not scoring_engine.validate_point_values(new_point_values):
            return HTMLResponse(
                f'<div class="text-red-600 bg-red-50 border border-red-200 rounded-md p-4">❌ Invalid point values. All values must be non-negative integers.</div>',
                status_code=400
            )
        
        # Update user's point values in database
        await update_user_point_values(db, current_user.id, new_point_values)
        
        # Recalculate all engagement scores for this user
        recalculated_count = await scoring_engine.recalculate_user_scores(
            current_user.id, 
            new_point_values, 
            db
        )
        
        # Get updated user data
        updated_user = await get_user_by_id(db, current_user.id)
        
        # Return success message with updated values
        return HTMLResponse(f'''
        <div class="text-green-600 bg-green-50 border border-green-200 rounded-md p-4 mb-4">
            ✅ Point values updated successfully! {recalculated_count} engagement scores recalculated.
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div class="text-center">
                    <p class="text-sm font-medium text-blue-600">Likes</p>
                    <p class="text-2xl font-bold text-blue-900">{new_point_values['like']}</p>
                </div>
            </div>
            <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                <div class="text-center">
                    <p class="text-sm font-medium text-green-600">Retweets</p>
                    <p class="text-2xl font-bold text-green-900">{new_point_values['retweet']}</p>
                </div>
            </div>
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <div class="text-center">
                    <p class="text-sm font-medium text-yellow-600">Replies</p>
                    <p class="text-2xl font-bold text-yellow-900">{new_point_values['reply']}</p>
                </div>
            </div>
            <div class="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <div class="text-center">
                    <p class="text-sm font-medium text-purple-600">Mentions</p>
                    <p class="text-2xl font-bold text-purple-900">{new_point_values['mention']}</p>
                </div>
            </div>
        </div>
        
        <div class="bg-blue-50 border border-blue-200 rounded-md p-4">
            <h3 class="text-sm font-medium text-blue-800 mb-2">Impact Summary</h3>
            <div class="text-sm text-blue-700 space-y-1">
                <p>• 1 like = {new_point_values['like']} points</p>
                <p>• 1 retweet = {new_point_values['retweet']} points</p>
                <p>• 1 reply = {new_point_values['reply']} points</p>
                <p>• 1 mention = {new_point_values['mention']} points</p>
            </div>
        </div>
        ''')
        
    except Exception as e:
        print(f"Error updating point values: {e}")
        return HTMLResponse(
            f'<div class="text-red-600 bg-red-50 border border-red-200 rounded-md p-4">❌ Error updating point values: {str(e)}</div>',
            status_code=500
        )

@router.get("/api/current-points", response_class=JSONResponse)
async def get_current_point_values(
    current_user: User = Depends(get_current_user),
    db=Depends(get_db)
):
    """API endpoint to get current user point values"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        # Get fresh user data
        user = await get_user_by_id(db, current_user.id)
        return {
            "point_values": user.point_values,
            "user_id": user.id
        }
    except Exception as e:
        print(f"Error getting point values: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving point values")

@router.get("/api/point-impact", response_class=JSONResponse)
async def get_point_impact_analysis(
    current_user: User = Depends(get_current_user),
    db=Depends(get_db)
):
    """API endpoint to analyze how current point values affect engagement scoring"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        current_points = current_user.point_values
        
        # Calculate impact analysis
        impact_analysis = {
            "current_values": current_points,
            "scoring_formula": f"(likes × {current_points['like']}) + (retweets × {current_points['retweet']}) + (replies × {current_points['reply']}) + (mentions × {current_points['mention']})",
            "example_scenarios": {
                "high_engagement": {
                    "likes": 100,
                    "retweets": 50,
                    "replies": 25,
                    "mentions": 10,
                    "score": (100 * current_points['like']) + (50 * current_points['retweet']) + (25 * current_points['reply']) + (10 * current_points['mention'])
                },
                "medium_engagement": {
                    "likes": 50,
                    "retweets": 25,
                    "replies": 10,
                    "mentions": 5,
                    "score": (50 * current_points['like']) + (25 * current_points['retweet']) + (10 * current_points['reply']) + (5 * current_points['mention'])
                },
                "low_engagement": {
                    "likes": 10,
                    "retweets": 5,
                    "replies": 2,
                    "mentions": 1,
                    "score": (10 * current_points['like']) + (5 * current_points['retweet']) + (2 * current_points['reply']) + (1 * current_points['mention'])
                }
            },
            "recommendations": {
                "high_value_actions": [],
                "optimization_tips": []
            }
        }
        
        # Determine high value actions
        sorted_actions = sorted(current_points.items(), key=lambda x: x[1], reverse=True)
        impact_analysis["recommendations"]["high_value_actions"] = [
            f"Focus on {action} (worth {points} points)" for action, points in sorted_actions[:2]
        ]
        
        # Generate optimization tips
        if current_points['reply'] > current_points['like']:
            impact_analysis["recommendations"]["optimization_tips"].append(
                "Replies are worth more than likes - encourage conversation!"
            )
        if current_points['retweet'] > current_points['like']:
            impact_analysis["recommendations"]["optimization_tips"].append(
                "Retweets are high-value - create shareable content!"
            )
        if current_points['mention'] == current_points['like']:
            impact_analysis["recommendations"]["optimization_tips"].append(
                "Mentions and likes have equal value - both are important!"
            )
        
        return impact_analysis
        
    except Exception as e:
        print(f"Error analyzing point impact: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing point impact")
