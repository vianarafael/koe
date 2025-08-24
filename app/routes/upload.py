from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from app.auth import get_current_user
from app.models import User, CSVUploadResponse
from app.db import get_db, store_multiple_engagements
from app.csv_parser import csv_parser
from app.templates import get_templates

router = APIRouter(prefix="/upload", tags=["file upload"])
templates = get_templates()

@router.get("/", response_class=HTMLResponse)
async def upload_page(request: Request, current_user: User = Depends(get_current_user)):
    """Display CSV upload page"""
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=302)
    
    return templates.TemplateResponse("upload.html", {
        "request": request, 
        "current_user": current_user
    })

@router.post("/csv")
async def upload_csv(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db=Depends(get_db)
):
    """Handle CSV file upload and parsing"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    # Validate file type
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    try:
        # Parse CSV file
        engagements, parse_errors = await csv_parser.parse_csv_file(file, current_user.id)
        
        if not engagements:
            raise HTTPException(status_code=400, detail="No valid engagement data found in CSV")
        
        # Store engagements in database
        stored_count = await store_multiple_engagements(db, engagements)
        
        # Prepare response
        response = CSVUploadResponse(
            message=f"Successfully processed {len(engagements)} records",
            records_processed=len(engagements),
            records_stored=stored_count,
            errors=[f"Row {error.row}: {error.error}" for error in parse_errors]
        )
        
        # Redirect to dashboard with success message
        return RedirectResponse(
            url=f"/?upload_success=true&processed={len(engagements)}&stored={stored_count}&errors={len(parse_errors)}", 
            status_code=302
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other errors
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/sample")
async def download_sample_csv(request: Request, current_user: User = Depends(get_current_user)):
    """Download a sample CSV file for reference"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Create sample CSV content
    sample_csv = """Tweet ID,Tweet text,Posted date,Likes,Retweets,Replies,Mentions
1234567890123456789,This is a sample tweet,2024-01-15 14:30:00,42,12,8,3
9876543210987654321,Another sample tweet with engagement,2024-01-14 10:15:00,128,45,23,7
5556667778889990000,Third sample tweet,2024-01-13 16:45:00,67,18,12,2"""
    
    from fastapi.responses import Response
    return Response(
        content=sample_csv,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=sample_engagement_data.csv"}
    )
