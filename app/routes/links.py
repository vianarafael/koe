from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from typing import Optional
from datetime import datetime
from app.auth import get_current_user
from app.models import User, TrackedLink, TrackedLinkCreate, SourceType
from app.db import get_db, create_tracked_link, get_user_tracked_links, delete_tracked_link, get_site_by_id, get_user_sites
from app.templates import get_templates
import secrets
import string

router = APIRouter(prefix="/links", tags=["links"])
templates = get_templates()

def generate_short_code(length: int = 6) -> str:
    """Generate a random short code for URLs"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@router.get("/", response_class=HTMLResponse)
async def links_page(request: Request, current_user: User = Depends(get_current_user)):
    """Display link management page"""
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=302)
    
    # Get user's sites and links
    db = await get_db()
    sites = await get_user_sites(db, current_user.id)
    links = await get_user_tracked_links(db, current_user.id)
    await db.close()
    
    template = templates.get_template("links.html")
    return HTMLResponse(template.render(
        request=request,
        current_user=current_user,
        sites=sites,
        links=links,
        now=datetime.now()
    ))

@router.post("/", response_class=HTMLResponse)
async def create_link_route(
    request: Request,
    site_id: str = Form(...),
    original_url: str = Form(...),
    source: str = Form(...),
    campaign: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    """Create a new tracked link"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if not original_url or not original_url.strip():
        raise HTTPException(status_code=400, detail="Original URL is required")
    
    if not site_id:
        raise HTTPException(status_code=400, detail="Site is required")
    
    if not source or source not in ['x', 'reddit', 'linkedin', 'other']:
        raise HTTPException(status_code=400, detail="Invalid source")
    
    # Validate that user owns the site
    db = await get_db()
    site = await get_site_by_id(db, site_id, current_user.id)
    if not site:
        await db.close()
        raise HTTPException(status_code=400, detail="Site not found or access denied")
    
    # Basic URL validation
    original_url = original_url.strip()
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url
    
    # Validate that URL belongs to the site
    from urllib.parse import urlparse
    parsed_url = urlparse(original_url)
    if not parsed_url.netloc.endswith(site.domain) and parsed_url.netloc != site.domain:
        await db.close()
        raise HTTPException(status_code=400, detail="URL must belong to the selected site")
    
    try:
        # Generate short code
        short_code = generate_short_code()
        
        # Set UTM parameters
        utm_source = source
        utm_medium = "social"
        utm_campaign = campaign or "link_tracking"
        
        # Create tracked link
        new_link = await create_tracked_link(
            db, current_user.id, site_id, original_url, 
            source, short_code, utm_source, utm_medium, utm_campaign
        )
        
        await db.close()
        
        # Redirect back to links page with success message
        return RedirectResponse(url=f"/links?success=created&short_code={short_code}", status_code=302)
        
    except Exception as e:
        await db.close()
        raise HTTPException(status_code=500, detail=f"Failed to create link: {str(e)}")

@router.delete("/{link_id}", response_class=JSONResponse)
async def delete_link_route(
    link_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a tracked link (soft delete)"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        db = await get_db()
        success = await delete_tracked_link(db, link_id, current_user.id)
        await db.close()
        
        if not success:
            raise HTTPException(status_code=404, detail="Link not found or access denied")
        
        return {"success": True, "message": "Link deleted successfully"}
        
    except Exception as e:
        await db.close()
        raise HTTPException(status_code=500, detail=f"Failed to delete link: {str(e)}")

@router.get("/api/list", response_class=JSONResponse)
async def list_links_api(current_user: User = Depends(get_current_user)):
    """API endpoint for getting user's tracked links"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        db = await get_db()
        links = await get_user_tracked_links(db, current_user.id)
        await db.close()
        
        return {"links": [link.dict() for link in links]}
        
    except Exception as e:
        await db.close()
        raise HTTPException(status_code=500, detail=f"Failed to fetch links: {str(e)}")

@router.get("/api/sites", response_class=JSONResponse)
async def list_sites_api(current_user: User = Depends(get_current_user)):
    """API endpoint for getting user's sites for link creation"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        db = await get_db()
        sites = await get_user_sites(db, current_user.id)
        await db.close()
        
        return {"sites": [site.dict() for site in sites]}
        
    except Exception as e:
        await db.close()
        raise HTTPException(status_code=500, detail=f"Failed to fetch sites: {str(e)}")
