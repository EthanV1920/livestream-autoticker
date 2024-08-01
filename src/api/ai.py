from pathlib import Path
from fastapi import APIRouter, Depends, Request
from src.api import auth
import sqlalchemy
import json
from openai import OpenAI

from src import database as db

# Object setup
client = OpenAI()
router = APIRouter(
        dependencies=[Depends(auth.get_api_key)],
        )

# Global setup
# GPT_MODEL = "gpt-4o"
GPT_MODEL = "gpt-4o-mini"


@router.get("/ticker/", tags=["ticker"])
def get_new_ticker(elapsed_time, prior_male_standings, current_male_standings, prior_female_standings, current_female_standings):
    """
        elapsed_time 
    """
    messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that will help to create a ticker message for a live stream that will last 30 hours. This live stream will be about the runners of the Western States Endurance Run which is a 100 mile run from Palisades Resort in Olympic Valley to Placer High School in Auburn California."
            },
            {
                "role": "system",
                "content": " You will make a 250 character comment for the male list and the female list. This comment should show any place changes and any advancements and overtakes on the field. This information should be presented in a professianal manner and should not be offensive. You will also mention both last names and first names when referring to a runner. You will output the two comments in order of male and female one after the other and only the comments."
            },
            {
                "role": "system",
                "content": "For both male and female runner, you will be given of the current standing and the standing from the last time the message was updated. You will also be given a list of aid stations with their record time and a small description about that aid station"
            },
            {
                "role": "system",
                "content": "This is an example of a good comment: Hayden Hawks moved from second place to firstplace in the mens field overtaking Jim Whamsley right out of the canyons as they entered the Devils Thumb Aid station."
            },
            {
                "role": "user",
                "content": f"This is the table for the male standing {elapsed_time} minuets ago: {prior_male_standings} and this is the current male standing: {current_male_standings}. This is the table for the female standing {elapsed_time} minuets ago: {prior_female_standings} and this is the current female standing: {current_female_standings}."
            }
                ]
    chat_response = chat_completion_request(messages)
    chat_message = chat_response.choices[0].message.content
    print(chat_message)
    print(f"Generated Mesasge: \n {chat_response}")
    sql_text = sqlalchemy.text("""
    insert into chat_history (message, valid)
    values (
      :message,
      :valid
    )
    """)

    sql_options = {
            "message": chat_message,
            "valid": 0
            }

    with db.engine.begin() as connection:
        result = connection.execute(sql_text, sql_options)

    print(result)

    return chat_response


def chat_completion_request(messages, tools=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            # tools=tools,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
