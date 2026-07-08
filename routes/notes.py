from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy import select,or_
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime,UTC
from schemas import NoteCreate,NoteResponse,UpdateNote,TrashNoteResponse,SortField,MessageResponse
from utils.jwt_handler import get_current_user
from models import Notes,User

router= APIRouter(prefix="/notes",tags= ["Notes"])


@router.post("/",response_model=NoteResponse)
def create_note(note: NoteCreate,
                db:Session= Depends(get_db),
                current_user:User = Depends(get_current_user)):
    
    new_note= Notes(
        title= note.title,
        content= note.content,
        user_id= current_user.id)
    
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note



@router.get("/",response_model= list[NoteResponse])
def get_notes(
                search: str| None = Query(default= None),
                sort: SortField | None = Query(default=None),
                descending: bool | None = Query(default=False),
                db:Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    query = select(Notes).where(Notes.user_id == current_user.id,Notes.is_deleted.is_(False),Notes.is_archived.is_(False))
    if search:
        query = query.where(or_(Notes.title.ilike(f"%{search}%"),Notes.content.ilike(f"%{search}%")))
    if sort:
        sort_expression = getattr(Notes,sort.value)
        order = sort_expression.desc() if descending else sort_expression.asc()
        query= query.order_by(Notes.is_pinned.desc(),order)
    else:
        query= query.order_by(Notes.is_pinned.desc(),Notes.last_updated.desc())
    
    notes= db.scalars(query).all()
    return notes

    
@router.patch("/{id}",response_model=NoteResponse)
def edit_note(id:int,
              update: UpdateNote,
              db: Session=Depends(get_db),
              current_user:User = Depends(get_current_user)):
    
    note = db.scalar(select(Notes).where(Notes.id == id,Notes.user_id == current_user.id))
    if not note:
        raise HTTPException(status_code=404,detail="Note not found")
    data= update.model_dump(exclude_unset= True)
    for field,value in data.items():
        setattr(note,field,value)
    if "is_deleted" in data:
         note.deleted_at = datetime.now(UTC) if note.is_deleted else None
    if not db.is_modified(note):
        return note
    db.commit()
    db.refresh(note)
    return note

@router.get("/trash",response_model=list[TrashNoteResponse])
def trash_notes(db: Session=Depends(get_db),
              current_user:User = Depends(get_current_user)):
    notes = db.scalars(select(Notes).where(Notes.user_id == current_user.id, Notes.is_deleted.is_(True))).all()
    return notes

@router.get("/archived",response_model=list[NoteResponse])
def archived_notes(db: Session=Depends(get_db),
              current_user:User = Depends(get_current_user)):
    notes = db.scalars(select(Notes).where(Notes.user_id == current_user.id, Notes.is_archived.is_(True))).all()
    return notes
    

@router.delete("/{id}",response_model= MessageResponse)
def permanent_delete_note(id:int,
              db: Session=Depends(get_db),
              current_user: User = Depends(get_current_user)):
    
    note = db.scalar(select(Notes).where(Notes.id == id,Notes.user_id == current_user.id))
    if not note:
        raise HTTPException(status_code=404,detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}


@router.get("/{id}",response_model=NoteResponse)
def show_note_by_id(id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    query = select(Notes).where(Notes.user_id == current_user.id,Notes.id == id)
    note = db.scalar(query)
    if note is None:
       raise HTTPException(status_code=404,detail = "Note not found")
    return note

