from fastapi import APIRouter, Response, encoders, responses
import sqlalchemy

from src import database as db

# Object setup
router = APIRouter()


@router.get("/data/", tags=["data"])
def test():

    message_sql = sqlalchemy.text("""
    select message
    from chat_history
    where live = 'True'
    limit 1
    """)

    with db.engine.begin() as connection:
        message = connection.execute(message_sql).fetchone()[0]
        print(f"DB Message: \n{message}")

    data = encoders.jsonable_encoder(message)
    return responses.JSONResponse(content=data)
