from pydantic import BaseModel, conint, constr, Field
from typing import Optional, List, Union, Pattern, Annotated
from datetime import datetime, timedelta
from enum import Enum
import json

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    idUser: int
    name: str
    username: str
    email: Optional[str] = None
    disabled: Union[bool, None] = None


## URL SHORTENER ##

class UrlInput(BaseModel):
    long_url: str

class UrlResponse(BaseModel):
    short_url: str
    long_url: str
