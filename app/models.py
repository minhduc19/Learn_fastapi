from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.types import Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.orm import Mapped
from .database import Base
from typing import List
from sqlalchemy.orm.collections import MappedCollection


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


    phrases = relationship("Phrase", back_populates="owner",foreign_keys= "Phrase.owner_id")
    authorPhrases = relationship("Phrase", back_populates="author",foreign_keys= "Phrase.author_id")


Phrase_entry = Table(
    "entry_phrase",
    Base.metadata,
    Column("entry_id", ForeignKey("entry.id"), primary_key=True),
    Column("phrase_id", ForeignKey("phrases.id"), primary_key=True))


class Phrase_entry1(Base):
    __tablename__ = "entry_phrase"
    __table_args__ = {'extend_existing': True}
    entry_id = Column(Integer, ForeignKey("entry.id"), primary_key=True)
    phrase_id = Column(Integer,ForeignKey("phrases.id"), primary_key=True)
    


class Phrase(Base):
    __tablename__ = "phrases"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    entries = relationship("Entry", secondary="entry_phrase", back_populates="phrases")
    owner = relationship("User",foreign_keys= "Phrase.owner_id",back_populates="phrases")
    author = relationship("User",foreign_keys= "Phrase.author_id",back_populates="authorPhrases")
    
    #owner = relationship("User",primaryjoin= "Phrase.owner_id == User.id",back_populates="phrases")

class Kanji(Base):
    __tablename__ = "kanji"
    id = Column(Integer, primary_key=True, index=True )
    idseq = Column(Integer, ForeignKey("entry.id"))
    text = Column(Text)

class Entry(Base):
    __tablename__ = "entry"
    id = Column(Integer, primary_key=True, index=True)
    idseq = Column(Integer)
    kanji = relationship("Kanji", foreign_keys=Kanji.idseq)
    phrases = relationship("Phrase", secondary="entry_phrase", back_populates="entries")