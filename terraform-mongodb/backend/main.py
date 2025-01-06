from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(title="MongoDB API")

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client.get_database("mydatabase")

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

@app.get("/")
async def root():
    return {"message": "MongoDB API is running"}

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    try:
        result = db.items.insert_one(item.dict())
        created_item = db.items.find_one({"_id": result.inserted_id})
        return {**created_item, "_id": str(created_item["_id"])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/", response_model=List[Item])
async def read_items():
    try:
        items = list(db.items.find())
        for item in items:
            item["_id"] = str(item["_id"])
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    try:
        from bson.objectid import ObjectId
        item = db.items.find_one({"_id": ObjectId(item_id)})
        if item:
            item["_id"] = str(item["_id"])
            return item
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    try:
        from bson.objectid import ObjectId
        result = db.items.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count:
            return {"message": "Item deleted successfully"}
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)