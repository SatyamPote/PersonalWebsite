from sqlalchemy.orm import Session
from .db import models
from .schemas import note as note_schema
from .schemas import link as link_schema

# --- User CRUD ---
def get_user_by_firebase_uid(db: Session, firebase_uid: str):
    return db.query(models.User).filter(models.User.firebase_uid == firebase_uid).first()

def create_user(db: Session, firebase_uid: str, email: str):
    db_user = models.User(firebase_uid=firebase_uid, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Note CRUD ---
def get_notes_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Note).filter(models.Note.owner_id == user_id).order_by(models.Note.id.desc()).all()

def create_user_note(db: Session, note: note_schema.NoteCreate, user_id: int):
    db_note = models.Note(**note.model_dump(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int, user_id: int):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == user_id).first()
    if note:
        db.delete(note)
        db.commit()
    return note

# --- Media File CRUD ---
def get_media_files_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.MediaFile).filter(models.MediaFile.owner_id == user_id).order_by(models.MediaFile.id.desc()).all()

def create_media_file_record(db: Session, user_id: int, filename: str, file_url: str, file_type: str):
    db_media_file = models.MediaFile(owner_id=user_id, filename=filename, file_url=file_url, file_type=file_type)
    db.add(db_media_file)
    db.commit()
    db.refresh(db_media_file)
    return db_media_file

def delete_media_file(db: Session, media_id: int, user_id: int):
    media = db.query(models.MediaFile).filter(models.MediaFile.id == media_id, models.MediaFile.owner_id == user_id).first()
    if media:
        # Note: This only deletes the DB record, not the file from Cloudinary.
        # A more advanced implementation would also call Cloudinary's delete API.
        db.delete(media)
        db.commit()
    return media

# --- Saved Link CRUD ---
def get_saved_links_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.SavedLink).filter(models.SavedLink.owner_id == user_id).order_by(models.SavedLink.created_at.desc()).all()

def create_saved_link(db: Session, link: link_schema.SavedLinkCreate, user_id: int):
    db_link = models.SavedLink(url=str(link.url), title=link.title, description=link.description, category=link.category, owner_id=user_id)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

def delete_saved_link(db: Session, link_id: int, user_id: int):
    link = db.query(models.SavedLink).filter(models.SavedLink.id == link_id, models.SavedLink.owner_id == user_id).first()
    if link:
        db.delete(link)
        db.commit()
    return link