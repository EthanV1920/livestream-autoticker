from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import ai, test
import json
import logging
import sys
from starlette.middleware.cors import CORSMiddleware

description = """
WSER Live Stream Ticker Utility
"""

app = FastAPI(
    title="Auto Ticker",
    description=description,
    version="0.0.1",
    terms_of_service="NA",
    contact={
        "name": "Ethan Vosburg",
        "email": "vosburgproductions@gmail.com",
    },
)

# origins = ["https://potion-exchange.velupierce@calpoly.edurcel.app"]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(ai.router)
app.include_router(test.router)
# app.include_router(handler.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "WSER Auto Ticker"}

