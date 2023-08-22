from pydantic import BaseModel
from typing import List, Optional

class PhraseBase(BaseModel):
    description: str | None = None

    class Config:
        orm_mode = True
        from_attributes=True

class EntryBase(BaseModel):
    id: int
    class Config:
        orm_mode = True
        from_attributes=True

class UserBase(BaseModel):
    email: str
    class Config:
        orm_mode = True
        from_attributes=True

class PhraseSchema(PhraseBase):
    entries: List[EntryBase]
    owner: UserBase


class EntrySchema(BaseModel):
    phrases: List[PhraseBase]


class PhraseCreate(PhraseBase):
    pass

class Phrase(PhraseBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    is_active: bool
    items: list[Phrase] = []

    class Config:
        orm_mode = True