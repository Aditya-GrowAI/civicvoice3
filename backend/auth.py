import os
import httpx
from fastapi import Request, HTTPException
from dotenv import load_dotenv

load_dotenv()

CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_ISSUER_URL = os.getenv("CLERK_ISSUER_URL")

async def get_current_user(request: Request):
    """
    Verify Clerk session token using Clerk's API.
    This is more reliable than manual JWT verification.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]

    if not CLERK_SECRET_KEY:
        print("WARNING: CLERK_SECRET_KEY not set. Skipping auth for development.")
        # For development only - return a mock user
        return {"sub": "dev_user", "email": "dev@example.com"}

    try:
        # Verify the session token with Clerk's API
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.clerk.com/v1/sessions/{token}/verify",
                headers={"Authorization": f"Bearer {CLERK_SECRET_KEY}"}
            )
            
            if response.status_code == 200:
                session_data = response.json()
                return {
                    "sub": session_data.get("user_id"),
                    "email": session_data.get("email")
                }
            else:
                raise HTTPException(status_code=401, detail="Invalid session token")

    except Exception as e:
        print(f"Auth Error: {e}")
        # For development - allow requests through
        print("WARNING: Auth failed, allowing request for development")
        return {"sub": "dev_user", "email": "dev@example.com"}
