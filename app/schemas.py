from pydantic import BaseModel
from typing import List, Optional

class WordCreate(BaseModel):
    word: str

class WordResponse(BaseModel):
    word: str
    definitions: Optional[List[str]] = None
    synonyms: Optional[List[str]] = None
    translations: Optional[List[str]] = None
    examples: Optional[List[str]] = None
