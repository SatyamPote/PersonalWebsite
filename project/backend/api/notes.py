from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud import crud
from schemas import note as note_schema
from db import models
from dependencies import get_db, get_current_user
import crud

router = APIRouter()

@router.post("/", response_model=note_schema.Note)
def create_note(note: note_schema.NoteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_user_note(db=db, note=note, user_id=current_user.id)

@router.get("/", response_model=List[note_schema.Note])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_notes_by_user(db, user_id=current_user.id, skip=skip, limit=limit)

@router.delete("/{note_id}", status_code=status.HTTP_200_OK)
def delete_user_note(note_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    deleted_note = crud.delete_note(db=db, note_id=note_id, user_id=current_user.id)
    if not deleted_note:
        raise HTTPException(status_code=404, detail="Note not found or you don't have permission to delete it.")
    return {"status": "success", "message": "Note deleted successfully"}