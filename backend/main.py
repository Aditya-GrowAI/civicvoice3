from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from database import db
from models import Issue
from auth import get_current_user
from gemini import detect_issue
from email_service import send_issue_email
import os
import uuid
from pydantic import BaseModel

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    try:
        if db is not None:
            await db.command("ping")
            print("INFO:     Successfully connected to MongoDB!")
        else:
            print("WARNING:  MongoDB client not initialized.")
    except Exception as e:
        print(f"ERROR:    Could not connect to MongoDB: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev, restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

class RequestIn(BaseModel):
    description: str
    latitude: float
    longitude: float

@app.get("/")
def root():
    return {"status": "API is running (MongoDB + Clerk)"}

# ---------------- CREATE REQUEST (Manual) ----------------
@app.post("/requests")
async def create_request(
    data: RequestIn, 
    user: dict = Depends(get_current_user)
):
    """
    Creates a manual issue request.
    Requires Authentication.
    """
    issue_data = {
        "id": str(uuid.uuid4()),
        "description": data.description,
        "lat": data.latitude,
        "lng": data.longitude,
        "status": "Pending",
        "type": "Manual",
        "user_id": user.get("sub"), # storing the Clerk User ID
        "image": None
    }

    # Insert into MongoDB
    if db is not None:
        await db.issues.insert_one(issue_data)
        
        # We can also store the user context if we want to save local user data
        # await db.users.update_one({"id": user["sub"]}, {"$set": {"email": ...}}, upsert=True)
    else:
         raise HTTPException(status_code=500, detail="Database not connected")

    # Send Email
    try:
        send_issue_email(issue_data)
    except Exception as e:
        print(f"Email failed: {e}")

    return {"msg": "Request stored & email sent", "id": issue_data["id"]}


# ---------------- UPLOAD ISSUE (Image) ----------------
@app.post("/upload")
async def upload(
    file: UploadFile = File(...),
    lat: float = Form(...),
    lng: float = Form(...),
    description: str = Form(""),
    user: dict = Depends(get_current_user)
):
    """
    Uploads an image, detects issue using Gemini, and saves to DB.
    Requires Authentication.
    """
    try:
        image_bytes = await file.read()
        filename = f"{UPLOAD_DIR}/{uuid.uuid4()}.jpg"
        
        with open(filename, "wb") as f:
            f.write(image_bytes)

        # AI Detection
        label = detect_issue(image_bytes)

        issue_data = {
            "id": str(uuid.uuid4()),
            "type": label,
            "lat": lat,
            "lng": lng,
            "status": "Pending",
            "image": filename,
            "description": description,
            "user_id": user.get("sub")
        }

        if db is not None:
            await db.issues.insert_one(issue_data)
        else:
             raise HTTPException(status_code=500, detail="Database not connected")

        # Email notification
        try:
            send_issue_email(issue_data, filename)
        except Exception as e:
            print("Email failed:", e)

        return {
            "success": True,
            "issue": issue_data
        }

    except Exception as e:
        print(f"Upload Error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


# ---------------- GET ALL ISSUES ----------------
@app.get("/issues")
async def get_issues():
    """
    Public endpoint to view all issues (or restrict if needed).
    """
    if db is None:
         raise HTTPException(status_code=500, detail="Database not connected")
         
    issues_cursor = db.issues.find()
    issues = await issues_cursor.to_list(length=100)
    
    # helper to clean up _id if needed, though we used custom 'id' field
    for i in issues:
        if "_id" in i:
            i.pop("_id")
            
    return issues
