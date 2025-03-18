import random
import string
from fastapi import HTTPException

from models.validations import (
    UrlResponse, UrlInput
)

from .db import (
    add_url, get_url, list_urls
)

async def shorten_url(url: str) -> UrlResponse:
    """
    Shorten a URL by generating a random string.
    """

    print(f"Shortening URL: {url}")

    # Generate a unique short URL and save it
    for _ in range(3):  # Limit attempts to avoid infinite loops
        short_url = generate_short_url()
        if not get_url(short_url):
            try:
                add_url(short_url, url)
                resp = {
                    "short_url": short_url,
                    "long_url": url
                }
                return resp
            except Exception:
                raise HTTPException(status_code=500, detail="Error saving URL to database")
    raise HTTPException(status_code=500, detail="Failed to generate a unique short URL")




def generate_short_url(length=6) -> str:
    """
    Generate a random short URL using a secure random generator.
    """

    characters = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(characters) for _ in range(length))
