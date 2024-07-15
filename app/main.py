from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List

from .models import Word
from .schemas import WordCreate, WordResponse
from .crud import get_word, create_word, get_words, delete_word as delete_word_from_db
from .scraper import scrape_word
from .database import connect_to_mongo, close_mongo_connection

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/words/{word}", response_model=WordResponse, response_model_exclude_unset=True)
async def read_word(word: str):
    existing_word = await get_word(word)
    if existing_word:
        return existing_word

    word_details = scrape_word(word)
    if not word_details:
        raise HTTPException(status_code=404, detail="Word not found in Google Translate")

    word_data = Word(**word_details)
    await create_word(word_data)
    return word_data

@app.get("/words/", response_model=List[WordResponse], response_model_exclude_unset=True)
async def read_words(skip: int = 0, limit: int = 10, search: Optional[str] = None, 
                     sort_by: Optional[str] = Query(None, enum=["", "word"]), 
                     include_definitions: bool = Query(False), include_synonyms: bool = Query(False), 
                     include_translations: bool = Query(False), include_examples: bool = Query(True)):
    words = await get_words(skip=skip, limit=limit, search=search, sort_by=sort_by,
                            include_definitions=include_definitions, include_synonyms=include_synonyms, 
                            include_translations=include_translations, include_examples=include_examples)
    return words

@app.delete("/words/{word}", response_model=WordResponse, response_model_exclude_unset=True)
async def delete_word_endpoint(word: str):
    word_data = await get_word(word)
    if not word_data:
        raise HTTPException(status_code=404, detail="Word not found")
    await delete_word_from_db(word)
    return word_data
