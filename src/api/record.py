from fastapi import APIRouter, Response, encoders, responses
import datetime
import sqlalchemy
import requests
import json

from src import database as db

# Object setup
router = APIRouter()

# ultralive.net endpoint url
ul_overall = "https://www.ultralive.net/api/overall/stats/107"
ul_leaders = "https://www.ultralive.net/api/leaders/107/1"
ul_top_men = " https://www.ultralive.net/api/leaders/107/2"
ul_top_women = "https://www.ultralive.net/api/leaders/107/3"


@router.get("/record/", tags=["record"])
def record():
    now = datetime.datetime.now()
    start_time_datetime = now - datetime.datetime.fromtimestamp(1722657600)
    print(f"Current time: {start_time_datetime}")

    leaders_request = requests.get(ul_leaders)
    overall_request = requests.get(ul_overall)
    men_request = requests.get(ul_top_men)
    women_request = requests.get(ul_top_women)

    overall_parsed = overall_request.json()
    leaders_parsed = leaders_request.json()
    men_parsed = men_request.json()
    women_parsed = women_request.json()

    print(f"Overall Stats from ultralive:\n{overall_parsed}")
    print(f"Leaders Stats from ultralive:\n{leaders_parsed}")


    message_sql = sqlalchemy.text("""
    insert into waldo_test_data (overall, leaders, top_men, top_women, race_time)
    values (:overall, :leaders, :top_men, :top_women, :race_time)
    """)

    message_options = { 
                       "overall": json.dumps(overall_parsed),
                       "leaders": json.dumps(leaders_parsed),
                       "top_men": json.dumps(men_parsed),
                       "top_women": json.dumps(women_parsed),
                       "race_time": start_time_datetime
                       }

    with db.engine.begin() as connection:
        connection.execute(message_sql, message_options)
        # print(f"DB Response: \n{message}")

    return "200: OK"
