from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud
from ..schemas import link as link_schema
from ..db import models
from ..dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/", response_model=link_schema.SavedLink)
def create_link(link: link_schema.SavedLinkCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_saved_link(db=db, link=link, user_id=current_user.id)

@router.get("/", response_model=List[link_schema.SavedLink])
def read_links(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_saved_links_by_user(db, user_id=current_user.id, skip=skip, limit=limit)

@router.delete("/{link_id}", status_code=status.HTTP_200_OK)
def delete_user_link(link_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    deleted_link = crud.delete_saved_link(db=db, link_id=link_id, user_id=current_user.id)
    if not deleted_link:
        raise HTTPException(status_code=404, detail="Link not found or you don't have permission to delete it.")
    return {"status": "success", "message": "Link deleted successfully"}