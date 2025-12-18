import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()

API_KEY = str(os.getenv("ACCESS_API_KEY"))

def verify_api_key(x_api_key: str = Header(...)):
    """
    Verify the API key in the request against the predefined API key.

    Args:
        x_api_key (str): The API key provided in the request.

    Raises:
        HTTPException: If the API key is invalid, a 401 Unauthorized
            exception will be raised.
    """
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
