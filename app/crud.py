from app.models import Word
from app.database import db

async def get_word(word: str):
    return await db.database.words.find_one({"word": word}, {"_id": 0})

async def create_word(word: Word):
    await db.database.words.insert_one(word.dict())

async def get_words(skip: int, limit: int, search: str = None, sort_by: str = None,
                    include_definitions: bool = False, include_synonyms: bool = False, 
                    include_translations: bool = False, include_examples: bool = True):
    query = {}
    projection = {"_id": 0, "word": 1}
    
    if search:
        query["word"] = {"$regex": search, "$options": "i"}

    if include_definitions:
        projection["definitions"] = 1
    if include_synonyms:
        projection["synonyms"] = 1
    if include_translations:
        projection["translations"] = 1
    if include_examples:
        projection["examples"] = 1

    cursor = db.database.words.find(query, projection).skip(skip).limit(limit)
    
    if sort_by:
        sort_order = 1  # Ascending order
        if sort_by.startswith('-'):
            sort_order = -1  # Descending order
            sort_by = sort_by[1:]  # Remove the '-' prefix
        cursor = cursor.sort(sort_by, sort_order)

    return await cursor.to_list(length=limit)

async def delete_word(word: str):
    return await db.database.words.delete_one({"word": word})
