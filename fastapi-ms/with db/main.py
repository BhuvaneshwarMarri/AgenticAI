from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from contextlib import asynccontextmanager

from database import engine, Base, get_db
from models import Item
from schemas import ItemCreate, ItemUpdate, ItemResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # Application runs here

    # Shutdown logic (optional)
    await engine.dispose()

app = FastAPI(title="FastAPI CRUD with SQLite",lifespan=lifespan)

#GET
@app.get("/items", response_model=list[ItemResponse])
async def get_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item))
    return result.scalars().all()


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item

#POST
@app.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    new_item = Item(**item.model_dump())

    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)

    return new_item

#PUT
@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item: ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Item).where(Item.id == item_id))
    existing_item = result.scalar_one_or_none()

    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    existing_item.name = item.name
    existing_item.price = item.price
    existing_item.description = item.description

    await db.commit()
    await db.refresh(existing_item)

    return existing_item

#PATCH
@app.patch("/items/{item_id}", response_model=ItemResponse)
async def patch_item(
    item_id: int,
    item: ItemUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Item).where(Item.id == item_id))
    existing_item = result.scalar_one_or_none()

    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(existing_item, key, value)

    await db.commit()
    await db.refresh(existing_item)

    return existing_item

#DELETE
@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    await db.commit()

    return {"message": "Item deleted successfully"}