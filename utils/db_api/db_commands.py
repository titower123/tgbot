from typing import List

from sqlalchemy import and_

from utils.db_api.model import Items

async def add_items(**kwargs):
    newitem = await Items(**kwargs).create()
    return newitem

async def get_faculties() -> List[Items]:
    return await Items.query.distinct(Items.faculties_code).gino.all()

async def get_forma(facultie) -> List[Items]:
    return await Items.query.distinct(Items.form_code).where(Items.faculties_code == facultie).gino.all()

async def get_specialization(facultie, form) -> List[Items]:
    return await Items.query.distinct(Items.specialization_code).where(and_(Items.faculties_code == facultie, Items.form_code == form)).gino.all()

async def get_directions(facultie, form, specialization) -> List[Items]:
    items = await Items.query.where(
        and_(Items.faculties_code == facultie,
        Items.form_code == form,
        Items.specialization_code == specialization)
    ).gino.all()
    return items

async def get_direction(item_id) -> Items:
    item = await Items.query.where(Items.id == item_id).gino.first()
    return item