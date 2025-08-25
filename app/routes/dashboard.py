from fastapi import APIRouter, Request, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from typing import Optional, List
from app.auth import get_current_user
from app.models import User, TweetEngagement
from app.db import get_db, get_user_engagements, get_user_total_score, get_top_engagements, get_engagements_by_score_range
from app.templates import get_templates

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
templates = get_templates()

@router.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    """Display engagement dashboard"""
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=302)
    
    # Get user engagements
    engagements = await get_user_engagements(db, current_user.id, limit=100)
    
    # Calculate statistics
    stats = calculate_engagement_stats(engagements)
    
    # Get total score for consistency
    total_score = await get_user_total_score(db, current_user.id)
    
    template = templates.get_template("dashboard.html")
    return HTMLResponse(template.render(
        request=request,
        current_user=current_user,
        engagements=engagements,
        stats=stats,
        total_score=total_score
    ))

@router.get("/api/engagements", response_class=JSONResponse)
async def get_engagements_api(
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
    sort_by: str = Query("score", description="Sort by: score, date, engagement"),
    order: str = Query("desc", description="Order: asc, desc"),
    min_score: Optional[int] = Query(None, description="Minimum score filter"),
    max_score: Optional[int] = Query(None, description="Maximum score filter"),
    limit: int = Query(50, description="Number of results to return")
):
    """API endpoint for getting engagement data with sorting and filtering"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        # Get filtered data
        if min_score is not None or max_score is not None:
            min_score_val = min_score if min_score is not None else 0
            max_score_val = max_score
            tweets = await get_engagements_by_score_range(
                db, current_user.id, min_score_val, max_score_val, limit
            )
        else:
            tweets = await get_user_engagements(db, current_user.id, limit)
        
        # Sort the data
        tweets = sort_engagements(tweets, sort_by, order)
        
        # Convert to serializable format
        serializable_tweets = []
        for tweet in tweets:
            serializable_tweets.append({
                "id": tweet.id,
                "tweet_id": tweet.tweet_id,
                "tweet_text": tweet.tweet_text,
                "like_count": tweet.like_count,
                "retweet_count": tweet.retweet_count,
                "reply_count": tweet.reply_count,
                "mention_count": tweet.mention_count,
                "engagement_score": tweet.engagement_score,
                "posted_date": tweet.posted_date.isoformat() if tweet.posted_date else None,
                "fetched_at": tweet.fetched_at.isoformat()
            })
        
        return {
            "tweets": serializable_tweets,
            "total_count": len(serializable_tweets),
            "sort_by": sort_by,
            "order": order,
            "filters": {
                "min_score": min_score,
                "max_score": max_score,
                "limit": limit
            }
        }
        
    except Exception as e:
        print(f"Error in API endpoint: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving engagement data")

@router.get("/api/stats", response_class=JSONResponse)
async def get_stats_api(
    current_user: User = Depends(get_current_user),
    db=Depends(get_db)
):
    """API endpoint for getting engagement statistics"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        tweets = await get_user_engagements(db, current_user.id, limit=1000)
        stats = calculate_engagement_stats(tweets)
        
        return {
            "total_tweets": len(tweets),
            "total_score": stats["total_score"],
            "average_score": stats["average_score"],
            "top_score": stats["top_score"],
            "engagement_breakdown": stats["engagement_breakdown"]
        }
        
    except Exception as e:
        print(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Error calculating statistics")

def sort_engagements(engagements: List[TweetEngagement], sort_by: str, order: str) -> List[TweetEngagement]:
    """Sort engagements based on specified criteria"""
    reverse = order.lower() == "desc"
    
    if sort_by == "score":
        return sorted(engagements, key=lambda x: x.engagement_score, reverse=reverse)
    elif sort_by == "date":
        return sorted(engagements, key=lambda x: x.posted_date or x.fetched_at, reverse=reverse)
    elif sort_by == "engagement":
        # Sort by total engagement count (likes + retweets + replies + mentions)
        return sorted(engagements, key=lambda x: x.like_count + x.retweet_count + x.reply_count + x.mention_count, reverse=reverse)
    elif sort_by == "likes":
        return sorted(engagements, key=lambda x: x.like_count, reverse=reverse)
    elif sort_by == "retweets":
        return sorted(engagements, key=lambda x: x.retweet_count, reverse=reverse)
    elif sort_by == "replies":
        return sorted(engagements, key=lambda x: x.reply_count, reverse=reverse)
    else:
        # Default to score sorting
        return sorted(engagements, key=lambda x: x.engagement_score, reverse=True)

def calculate_engagement_stats(engagements: List[TweetEngagement]) -> dict:
    """Calculate engagement statistics from a list of engagements"""
    if not engagements:
        return {
            "total_score": 0,
            "average_score": 0,
            "top_score": 0,
            "engagement_breakdown": {"likes": 0, "retweets": 0, "replies": 0, "mentions": 0}
        }
    
    total_score = sum(e.engagement_score for e in engagements)
    average_score = total_score / len(engagements) if engagements else 0
    top_score = max(e.engagement_score for e in engagements) if engagements else 0
    
    # Calculate engagement breakdown
    total_likes = sum(e.like_count for e in engagements)
    total_retweets = sum(e.retweet_count for e in engagements)
    total_replies = sum(e.reply_count for e in engagements)
    total_mentions = sum(e.mention_count for e in engagements)
    
    return {
        "total_score": total_score,
        "average_score": round(average_score, 2),
        "top_score": top_score,
        "engagement_breakdown": {
            "likes": total_likes,
            "retweets": total_retweets,
            "replies": total_replies,
            "mentions": total_mentions
        }
    }
