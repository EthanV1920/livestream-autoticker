from pathlib import Path
from fastapi import APIRouter, Depends, Request, Response
from src.api import auth
import sqlalchemy
import json
from openai import OpenAI


# Object setup
router = APIRouter(
        # dependencies=[Depends(auth.get_api_key)],
        )


@router.get("/test/", tags=["test"])
def test():

    data = """
<rss version="2.0">

<channel>
<title>Local Testing</title>
<link>https://www.pythonbynight.com</link>
<description>Coolest Site Ever</description>

<item>
<title>Item Title</title>
<description>Such A Simple RSS Feed</description>
</item>
</channel>
</rss>
    """
    return Response(content=data, media_type="application/xml")
