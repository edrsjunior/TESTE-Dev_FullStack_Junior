import datetime
from dotenv import load_dotenv
import os

import jwt

load_dotenv()

KEY = os.getenv("MY_JWT_KEY")

def verifyJWTToken(token: str) ->int:
    decoded = jwt.decode(token,KEY, algorithms=["HS256"])
    
    return decoded['id']