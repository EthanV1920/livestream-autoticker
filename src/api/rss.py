from pathlib import Path
from fastapi import APIRouter, Depends, Request, Response
from src.api import auth
import sqlalchemy
import json
from openai import OpenAI

from src import database as db

# Object setup
router = APIRouter(
        # dependencies=[Depends(auth.get_api_key)],
        )


@router.get("/feed/", tags=["rss"])
def test():

    message_sql = sqlalchemy.text("""
    select message
    from chat_history
    where valid = 1
    """)

    with db.engine.begin() as connection:
        message = connection.execute(message_sql).fetchone()[0]
        print(f"DB Message: \n{message}")

    data = f"""
    <rss version="2.0">

    <channel>
    <title>Local Testing</title>
    <link>https://www.example.com</link>
    <description>Coolest Site Ever</description>

    <item>
    <title>{message}</title>
    </item>
    </channel>
    </rss>
    """
    return Response(content=data, media_type="application/xml")
