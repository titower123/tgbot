from typing import List
from sqlalchemy import and_
from utils.db_api.diractions import Directions
from utils.db_api.database import db


async def add_items(**kwargs):
    newitem = await Directions(**kwargs).create()
    return newitem


async def get_faculties() -> List[Directions]:
    return await Directions.query.distinct(Directions.faculties_code).gino.all()


async def get_forma(facultie) -> List[Directions]:
    return await Directions.query.distinct(Directions.form_code).where(Directions.faculties_code == facultie).gino.all()


async def get_specialization(facultie, form) -> List[Directions]:
    return await Directions.query.distinct(Directions.specialization_code).where(
        and_(Directions.faculties_code == facultie, Directions.form_code == form)).gino.all()


async def get_directions(facultie, form, specialization) -> List[Directions]:
    directions = await Directions.query.where(
        and_(Directions.faculties_code == facultie,
             Directions.form_code == form,
             Directions.specialization_code == specialization)
    ).gino.all()
    return directions


async def get_direction(item_id) -> Directions:
    item = await Directions.query.where(Directions.id == item_id).gino.first()
    return item


async def get_all_str():
    count = await db.func.count(Directions.id).gino.scalar()
    return await Directions.query.where(Directions.id < count + 1).gino.all()
