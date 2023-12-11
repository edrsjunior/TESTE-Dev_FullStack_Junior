import datetime
from dotenv import load_dotenv
import os

import jwt

load_dotenv()

KEY = os.getenv("MY_JWT_KEY")

def verifyJWTToken(token: str) ->bool:
    if not jwt.decode(token,KEY, algorithms=["HS256"]):
        return 0
    return 1