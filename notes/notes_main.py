from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

import models, schemas, crud
from database import engine, get_db
from routers_auth import router as auth_router
from auth import get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes app")

app.include_router(auth_router)

@app.post("/notes", response_model=schemas.Note)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_note(db=db, note=note, user_id=current_user.id)
@app.get("/notes", response_model=List[schemas.Note])
def read_notes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_notes(db, user_id=current_user.id)

@app.get("/notes/{note_id}", response_model=schemas.Note)
def read_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_note = crud.get_note(db, note_id=note_id, user_id=current_user.id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="заметка не найдена")
    return db_note

@app.put("/notes/{note_id}", response_model=schemas.Note)
def update_note(
    note_id: int,
    note_data: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_note = crud.update_note(db, note_id=note_id, user_id=current_user.id, note_data=note_data)
    if db_note is None:
        raise HTTPException(status_code=404, detail="заметка не найдена")
    return db_note

@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    success = crud.delete_note(db, note_id=note_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="заметка не найдена")
    return {"message": "заметка удалена успешно"}