import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from time import time

from models.validations import (
    Token, TokenData,
    UrlResponse, UrlInput
)

from helpers import (
    validate_user_login, user_authentication,
    shorten_url
)

# ====== LOGGING SETUP WITH ROTATION ====== #
log_file = "api_requests.log"

# Option 1: Size-Based Rotation (Keeps last 5 logs, each max 10MB)
log_handler = RotatingFileHandler(
    log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
)

# Option 2: Time-Based Rotation (Daily rotation, keeps logs for 7 days)
# log_handler = TimedRotatingFileHandler(
#     log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8"
# )

# Configure log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_handler.setFormatter(formatter)

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# ====== FASTAPI APP ====== #
app = FastAPI(
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    title="ART IA API",
    description="API to manage OpenAI integrations for NowMe app, and other projects",
)

# Middleware to log requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()
    body = await request.body()
    response = await call_next(request)
    process_time = time() - start_time

    log_message = (
        f"Method: {request.method} | Path: {request.url.path} | "
        f"Query Params: {request.query_params} | Body: {body.decode('utf-8')[:5000]} | "
        f"Response Status: {response.status_code} | Time: {process_time:.3f}s"
    )

    logger.info(log_message)
    return response

## PUBLIC ROUTES ##

@app.post("/token", response_model=Token, tags=["Obtain JWT token"], summary="Login route to get access token (JWT)")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return validate_user_login(form_data.username, form_data.password)

## PROTECTED ROUTES ##

# Shorten a URL
@app.post(
        "/shorten",
        tags=["URL Shortener"],
        summary="Shorten a URL",
        response_model=UrlResponse
        )
# async def shorten_url(url: UrlInput, authenticate: TokenData = Depends(user_authentication)):
async def generate_shorten_url(url_input: UrlInput):
    return await shorten_url(url_input.long_url)