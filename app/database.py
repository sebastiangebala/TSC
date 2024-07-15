from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient("mongodb://mongo:27017")
    db.database = db.client.translation_service

async def close_mongo_connection():
    db.client.close()
