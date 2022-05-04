from typing import List
from utils.db_api.quset import Question
from utils.db_api.database import db


async def add_question(user_id, message_id, question, date_time):
    await Question.create(user_id=str(user_id), message_id=message_id, question=question, date_and_time=date_time)


async def count_questions():
    return await db.func.count(Question.id).gino.scalar()


async def all_questions() -> List[Question]:
    return await Question.query.gino.all()


async def delete_question(question_id):
    await Question.delete.where(Question.id == int(question_id)).gino.status()


async def get_data_question(question_id) -> Question:
    return await Question.get(question_id)
