from typing import Union

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.dialects import postgresql
from . import models,schemas,crud
from .database import SessionLocal, engine, get_db
from .mapEntry import mapPhraseToEntry


models.Base.metadata.create_all(bind=engine)
print("test")
'''
with Session(bind=engine) as session:
    query = session.query(models.Phrase).options(joinedload(models.Phrase.entries), joinedload(models.Phrase.owner))
    #query = session.query(models.Phrase).join(models.User,models.User.id == models.Phrase.author_id)
    b1 = query.all()
print("sql is: " + str(query))
b1_schema = schemas.PhraseSchema.from_orm(b1[0])
print(b1_schema.model_dump_json())
#print(b1.owner.id)
print(str(b1[0]))
'''

with Session(bind=engine) as session:
    search = "{word}%".format(word = "食べ")
    query = session.query(models.Kanji).join(models.Entry,models.Entry.idseq == models.Kanji.idseq).filter(models.Kanji.text.like(search)).first()
#phraseRoot = mapPhraseToEntry("食べました")
#print(phraseRoot)
print("sql is: " + str(query))
print(str(query.idseq))

print(models.Base.metadata.tables)
app = FastAPI()



@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/phrases/", response_model=list[schemas.Phrase])
def read_phrases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_phrases(db, skip=skip, limit=limit)
    return users


@app.post("/users/{user_id}/items/", response_model=schemas.Phrase)
def create_item_for_user(
    user_id: int, phrase: schemas.PhraseCreate, db: Session = Depends(get_db)
):
    return crud.create_user_phrase(db=db, phrase=phrase, user_id=user_id)

@app.post("/users/{user_id}/phrases/", response_model=schemas.PhraseCreate)
def create_phrase_for_user(
    user_id: int, phrase: schemas.PhraseCreate, db: Session = Depends(get_db)
):
    user = crud.get_user_by_id(db,user_id)
    search = "{word}%".format(word = "食べ")
    entry = session.query(models.Kanji).join(models.Entry,models.Entry.idseq == models.Kanji.idseq).filter(models.Kanji.text.like(search)).first()
    entryPhrase = models.Phrase_entry1(entry_id = 1,phrase_id =9)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    new_phrase1 = models.Phrase(description=phrase.description,owner = user)
    phrase_entry = models.Phrase_entry1(entry_id = 1,phrase_id =25)
    db.add_all([new_phrase1,phrase_entry])
    db.commit()
    db.refresh(new_phrase1)
    return new_phrase1


""" 
@app.get("/phrases/")
def get_phrases(db: Session = Depends(get_db)):
    phrases = db.query(models.Phrase).all()
    return {"status":phrases}

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q} """