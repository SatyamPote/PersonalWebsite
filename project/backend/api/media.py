from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

import crud
from schemas import media as media_schema
from db import models
from dependencies import get_db, get_current_user  # Correct import
from services.storage import upload_file_to_cloudinary

router = APIRouter()

@router.post("/upload", response_model=media_schema.MediaFile)
def upload_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Handles file uploads for the authenticated user.
    """
    try:
        upload_result = upload_file_to_cloudinary(file)
        file_url = upload_result.get("secure_url")
        filename = upload_result.get("original_filename", file.filename)
        file_type = upload_result.get("resource_type", "raw")

        if not file_url:
            raise HTTPException(status_code=500, detail="Cloudinary did not return a file URL.")

        db_media_file = crud.create_media_file_record(
            db=db, user_id=current_user.id, filename=filename, file_url=file_url, file_type=file_type
        )
        return db_media_file

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during file upload: {e}")


@router.get("/", response_model=List[media_schema.MediaFile])
def read_media_files(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieve all media file records for the current authenticated user.
    """
    media_files = crud.get_media_files_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return media_files


@router.delete("/{media_id}", status_code=status.HTTP_200_OK)
def delete_user_media(
    media_id: int,
    db: Session = Depends(get_db),
    # THIS IS THE LINE THAT WAS FIXED (one underscore instead of two)
    current_user: models.User = Depends(get_current_user)
):
    """
    Delete a specific media record owned by the current authenticated user.
    """
    deleted_media = crud.delete_media_file(db=db, media_id=media_id, user_id=current_user.id)
    if not deleted_media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Media not found or you don't have permission to delete it."
        )
    return {"status": "success", "message": "Media record deleted successfully"}