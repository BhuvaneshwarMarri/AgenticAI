from fastapi import FastAPI, HTTPException
from typing import List
from models import Item

app = FastAPI(title="FastPI basic CRUD")

db: List[Item] = []


# GET REQUESTS
@app.get("/items", response_model=List[Item])
async def get_all_items():
    return db


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    for item in db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

#POST REQUEST
@app.post("/items", response_model=Item)
async def create_item(item: Item):
    for existing in db:
        if existing.id == item.id:
            raise HTTPException(status_code=400, detail="Item already exists")

    db.append(item)
    return item

# PUT REQUESTS
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(db):
        if item.id == item_id:
            db[index] = updated_item
            return updated_item

    raise HTTPException(status_code=404, detail="Item not found")

#PATCH REQUESTS
@app.patch("/items/{item_id}", response_model=Item)
async def patch_item(item_id: int, item_data: dict):
    for item in db:
        if item.id == item_id:
            if "name" in item_data:
                item.name = item_data["name"]
            if "price" in item_data:
                item.price = item_data["price"]
            if "description" in item_data:
                item.description = item_data["description"]

            return item

    raise HTTPException(status_code=404, detail="Item not found")

#DELETE REQUESTS

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for index, item in enumerate(db):
        if item.id == item_id:
            db.pop(index)
            return {"message": "Item deleted successfully"}

    raise HTTPException(status_code=404, detail="Item not found")