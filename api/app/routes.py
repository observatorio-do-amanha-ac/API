from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.drive import list_items_by_category, get_json_data_from_drive

router = APIRouter()

@router.get("/items/{category}")
async def get_items_by_category(category: str):
    items = list_items_by_category(category=category)
    return JSONResponse(content=items)

@router.get("/dataset/{id_planilha}")
async def get_dataset(id_planilha: str):
    dataset = get_json_data_from_drive(id_planilha)
    return JSONResponse(content=dataset)