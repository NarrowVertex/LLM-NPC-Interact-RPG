import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    name: str
    price: float


@router.post("/items/")
async def create_item(item: Item):
    return item


def get_app() -> FastAPI:

    app = FastAPI()

    app.include_router(router)
    return app

if __name__ == "__main__":
    uvicorn.run(get_app(), host="0.0.0.0", port=8000)


