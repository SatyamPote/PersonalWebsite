from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from crud import crud
from db.session import SessionLocal
from services.firebase_auth import verify_id_token

# This tells FastAPI that the token should be sent as a Bearer token in the Authorization header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    """Dependency to get a DB session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependency to get the current user.
    1. Verifies the Firebase ID token.
    2. Gets the user from our DB.
    3. If user doesn't exist, creates them.
    """
    try:
        user_data = verify_id_token(token)
        firebase_uid = user_data["uid"]
        email = user_data["email"]
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = crud.get_user_by_firebase_uid(db, firebase_uid=firebase_uid)
    if not user:
        # This is the user's first login, create an entry in our database
        user = crud.create_user(db, firebase_uid=firebase_uid, email=email)
        print(f"New user created in DB: {email} (UID: {firebase_uid})")

    return user