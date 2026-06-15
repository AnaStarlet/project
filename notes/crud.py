from sqlalchemy.orm import Session
import models, schemas

def get_note(db: Session, note_id: int, user_id: int):
    return db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == user_id
    ).first()


def get_notes(db: Session, user_id: int):
    return db.query(models.Note).filter(models.Note.owner_id == user_id).all()


def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(
        title=note.title,
        content=note.content,
        owner_id=user_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def update_note(db: Session, note_id: int, user_id: int, note_data: schemas.NoteUpdate):
    db_note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == user_id
    ).first()
    if not db_note:
        return None

    if note_data.title is not None:
        db_note.title = note_data.title
    if note_data.content is not None:
        db_note.content = note_data.content

    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int, user_id: int):
    db_note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == user_id
    ).first()
    if db_note:
        db.delete(db_note)
        db.commit()
        return True
    return False