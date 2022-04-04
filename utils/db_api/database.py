from gino import Gino
from data.config import POSTGRESURI

db = Gino()

async def create_db():
    await db.set_bind(POSTGRESURI)
    #await db.gino.create_all()