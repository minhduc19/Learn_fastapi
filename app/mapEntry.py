

from sqlalchemy.orm import Session, joinedload
from . import models
from .database import SessionLocal, engine
from typing import List
import MeCab
print("test")


def mapPhraseToEntry(japanesePhrase) -> str:
    wakati = MeCab.Tagger("-Owakati")
    listOfPhraseRoots= wakati.parse(japanesePhrase).split()
    phraseRoot = listOfPhraseRoots[0]
    return phraseRoot