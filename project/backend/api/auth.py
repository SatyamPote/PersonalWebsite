from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

from services.firebase_auth import verify_id_token

# This creates a new "router" object. We'll add all auth-related endpoints to it.
router = APIRouter()

# Define the data model for the incoming request
class Token(BaseModel):
    id_token: str

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_with_firebase(token: Token):
    """
    Receives a Firebase ID token, verifies it, and returns user info.
    This is the main authentication endpoint.
    """
    try:
        user_info = verify_id_token(token.id_token)
        
        # At this point, the user is authenticated.
        # Here you would typically find or create a user in your own database
        # and then issue your own access token (like a JWT).
        # For now, we'll just return the user info from Firebase.
        
        uid = user_info.get("uid")
        email = user_info.get("email")
        
        print(f"Successfully authenticated user: UID={uid}, Email={email}")
        
        return {
            "status": "success",
            "message": "User authenticated successfully.",
            "user": {
                "uid": uid,
                "email": email
            }
        }
    except ValueError as e:
        # This exception is raised from our service if the token is invalid
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )