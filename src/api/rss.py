from fastapi import APIRouter, Response
import sqlalchemy

from src import database as db

# Object setup
router = APIRouter()


@router.get("/feed/", tags=["rss"])
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
