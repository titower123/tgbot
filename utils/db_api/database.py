from gino import Gino
from gino.schema import GinoSchemaVisitor
from data.config import POSTGRESURI

db = Gino()

async def create_db():
    await db.set_bind(POSTGRESURI)
    await db.gino.create_all()