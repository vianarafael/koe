from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from typing import Optional
from datetime import datetime
from app.auth import get_current_user
from app.models import User, Site, SiteCreate
from app.db import get_db, create_site, get_user_sites, get_site_by_id, update_site, delete_site
from app.templates import get_templates

router = APIRouter(prefix="/sites", tags=["sites"])
templates = get_templates()

@router.get("/", response_class=HTMLResponse)
async def sites_page(request: Request, current_user: User = Depends(get_current_user)):
    """Display site management page"""
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=302)
    
    # Get user's sites
    db = await get_db()
    sites = await get_user_sites(db, current_user.id)
    await db.close()
    
    template = templates.get_template("sites.html")
    return HTMLResponse(template.render(
        request=request,
        current_user=current_user,
        sites=sites,
        now=datetime.now()
    ))

@router.post("/", response_class=HTMLResponse)
async def create_site_route(
    request: Request,
    domain: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    """Create a new site"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if not domain or not domain.strip():
        raise HTTPException(status_code=400, detail="Domain is required")
    
    # Basic domain validation
    domain = domain.strip().lower()
    if not domain or '.' not in domain:
        raise HTTPException(status_code=400, detail="Invalid domain format")
    
    try:
        db = await get_db()
        new_site = await create_site(db, current_user.id, domain)
        await db.close()
        
        # Redirect back to sites page with success message
        return RedirectResponse(url="/sites?success=created", status_code=302)
        
    except Exception as e:
        await db.close()
        raise HTTPException(status_code=500, detail=f"Failed to create site: {str(e)}")

@router.put("/{site_id}", response_class=JSONResponse)
async def update_site_route(
    site_id: str,
    domain: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    """Update a site's domain"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if not domain or not domain.strip():
        raise HTTPException(status_code=400, detail="Domain is required")
    
    # Basic domain validation
    domain = domain.strip().lower()
    if not domain or '.' not in domain:
        raise HTTPException(status_code=400, detail="Invalid domain format")
    
    try:
        db = await get_db()
        updated_site = await update_site(db, site_id, current_user.id, domain)
        await db.close()
        
        if not updated_site:
            raise HTTPException(status_code=404, detail="Site not found or access denied")
        
        return {"success": True, "site": updated_site.dict()}
        
    except Exception as e:
        await db.close()
        raise HTTPException(status_code=500, detail=f"Failed to update site: {str(e)}")

@router.delete("/{site_id}", response_class=JSONResponse)
async def delete_site_route(
    site_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a site (soft delete)"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        db = await get_db()
        success = await delete_site(db, site_id, current_user.id)
        await db.close()
        
        if not success:
            raise HTTPException(status_code=404, detail="Site not found or access denied")
        
        return {"success": True, "message": "Site deleted successfully"}
        
    except Exception as e:
        await db.close()
        raise HTTPException(status_code=500, detail=f"Failed to delete site: {str(e)}")

@router.get("/api/list", response_class=JSONResponse)
async def list_sites_api(current_user: User = Depends(get_current_user)):
    """API endpoint for getting user's sites"""
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
