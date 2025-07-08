from datetime import date
from fastapi import APIRouter, HTTPException
from fastapi.params import Query
from typing import List
from dal.db import async_session
from api import schemas
from dal import crud
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/rolls")

@router.get("/", response_model=List[schemas.RollRead])
async def get_all_rolls():
    async with async_session() as session:
        try:
            return await crud.get_all_rolls(session)
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Ошибка при получении списка рулонов")


@router.get("/{roll_id}", response_model=schemas.RollRead)
async def get_roll_by_id(roll_id: int):
    async with async_session() as session:
        try:
            roll = await crud.get_roll_by_id(session, roll_id)
            if not roll:
                raise HTTPException(status_code=404, detail="Рулон не найден")
            return roll
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Ошибка при получении рулона")

@router.get("/by_weight/", response_model=List[schemas.RollRead])
async def get_rolls_by_weight_range(min_weight: float = Query(..., description="Минимальный вес"), max_weight: float = Query(..., description="Максимальный вес")):
    async with async_session() as session:
        try:
            rolls = await crud.get_rolls_by_weight_range(session, min_weight, max_weight)
            return rolls
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Ошибка БД")

@router.get("/date_stat_count/", response_model=int)
async def get_rolls_count_in_period(date_from: date = Query(..., description="Начало периода"),date_to: date = Query(description="Конец периода")):
    async with async_session() as session:
        try:
            count = await crud.get_rolls_count_in_period(session, date_from, date_to)
            return count
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Ошибка БД")

@router.post("/", response_model=schemas.RollRead, status_code=201)
async def create_roll(roll: schemas.RollCreate):
    async with async_session() as session:
        try:
            return await crud.create_roll(session, roll)
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Ошибка при создании рулона")

@router.delete("/{roll_id}", response_model=schemas.RollRead)
async def delete_roll(roll_id: int):
    async with async_session() as session:
        try:
            deleted = await crud.delete_roll_by_id(session, roll_id)
            if not deleted:
                raise HTTPException(status_code=404, detail="Рулон не найден")
            return deleted
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Ошибка при удалении рулона")
