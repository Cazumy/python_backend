from dal.roll import Roll
from api.schemas import RollCreate
from typing import Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.exc import SQLAlchemyError

async def create_roll(session: AsyncSession, roll: RollCreate) -> Roll:
    try:
        new_roll = Roll(**roll.dict())
        session.add(new_roll)
        await session.commit()
        await session.refresh(new_roll)
        return new_roll
    except SQLAlchemyError:
        await session.rollback()
        raise

async def get_all_rolls(session: AsyncSession):
    try:
        result = await session.execute(select(Roll))
        return result.scalars().all()
    except NoResultFound:
        return None
    except SQLAlchemyError as e:
        await session.rollback()
        raise e

async def get_roll_by_id(session: AsyncSession, roll_id: int) -> Roll | None:
    try:
        return await session.get(Roll, roll_id)
    except NoResultFound:
        return None
    except SQLAlchemyError as e:
        await session.rollback()
        raise e

async def get_rolls_by_weight_range(session, min_weight: float, max_weight: float):
    try:
        query = select(Roll).where(
            Roll.weight >= min_weight,
            Roll.weight <= max_weight
        )
        result = await session.execute(query)
        return result.scalars().all()
    except SQLAlchemyError as e:
        await session.rollback()
        raise e

async def get_rolls_count_in_period(session, date_from, date_to: Optional[date] = None) -> int:
    try:
        conditions = [or_(Roll.date_of_adding == None, Roll.date_of_adding <= date_from)]
        if date_to is not None:
            conditions.append(or_(Roll.date_of_removing == None, Roll.date_of_removing >= date_to))
        else:
            conditions.append(True)
        query = select(func.count()).where(and_(*conditions))
        result = await session.execute(query)
        count = result.scalar()
        return count
    except SQLAlchemyError as e:
        await session.rollback()
        raise e
    
async def delete_roll_by_id(session: AsyncSession, roll_id: int) -> Roll | None:
    try:
        roll = await session.get(Roll, roll_id)
        if not roll:
            return None
        await session.delete(roll)
        await session.commit()
        return roll
    except SQLAlchemyError:
        await session.rollback()
        raise
