import random
import string
from fastapi import HTTPException, Response, status
import datetime

from models.validations import (
    UrlResponse, UrlInput, DeletedUrls, DeletedUrl
)

from .db import (
    add_url, get_url, list_urls, update_last_used, delete_url
)

# ====== URL SHORTENER ====== #

# Shorten URLs by generating a random string.
async def shorten_url(url: str) -> UrlResponse:
    """
    Shorten a URL by generating a random string.
    """

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
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error saving URL to database")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate a unique short URL")


# Retrieve a long URL from the database
async def get_long_url(short_url: str) -> UrlResponse:
    """
    Retrieve the long URL from the database using the short URL.
    """
    try:
        url = get_url(short_url)
        if url:
            update_last_used(short_url)
            # return {
            #     "short_url": short_url,
            #     "long_url": url.long_url
            # }
            return Response(status_code=status.HTTP_302_FOUND, headers={"Location": url.long_url})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving URL from database")
    
# Delete URLs that have not been used in the last 30 days
async def delete_inactive_urls() -> DeletedUrls:
    """
    Delete URLs that have not been used in the last 30 days.
    """
    try:
        urls = list_urls()
        deleted_urls = []
        for url in urls:
            if url.last_used < datetime.datetime.utcnow() - datetime.timedelta(days=30):
                delete_url(url.short_url)
                deleted_urls.append(DeletedUrl(
                    short_url=url.short_url,
                    long_url=url.long_url,
                    created_at=url.created_at,
                    last_used=url.last_used
                ))
        return DeletedUrls(
            deleted_urls=deleted_urls,
            deleted_count=len(deleted_urls),
            message="Deleted URLs that have not been used in the last 30 days"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting inactive URLs")

# ====== additional functions ====== #

# Generate a random string of fixed length
def generate_short_url(length=6) -> str:
    """
    Generate a random short URL using a secure random generator.
    """

    characters = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(characters) for _ in range(length))