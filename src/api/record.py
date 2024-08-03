from fastapi import APIRouter, Response, encoders, responses
import datetime
import sqlalchemy
import requests
import json

from src import database as db

# Object setup
router = APIRouter()

# ultralive.net endpoint url
ul_url = "https://www.ultralive.net/api/overall/stats/107"

# tz = pytz.timezone("America/Los_Angeles")
# start_time = datetime.datetime.strftime('%Y-%m-%d %H:%M:%S', localtime(1722682800))
# now = datetime.datetime.now(tz)

@router.get("/record/", tags=["record"])
def record():
    now = datetime.datetime.now()
    start_time_datetime = now - datetime.datetime.fromtimestamp(1722657600)
    print(f"Current time: {start_time_datetime}")

    overall_stat = requests.get(ul_url)
    parsed_overall_stat = overall_stat.json()
    print(f"Overall Stats from ultralive:\n{parsed_overall_stat}")


    message_sql = sqlalchemy.text("""
    insert into waldo_test_data (overall_stat, race_time)
    values (:json_data, :race_time)
    """)

    message_options = { 
                       "json_data": json.dumps(parsed_overall_stat),
                       "race_time": start_time_datetime
                       }

    with db.engine.begin() as connection:
        connection.execute(message_sql, message_options)
        # print(f"DB Response: \n{message}")

    return "200: OK"
