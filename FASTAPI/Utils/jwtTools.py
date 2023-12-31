import datetime
from dotenv import load_dotenv
import os
from fastapi import HTTPException

import jwt

load_dotenv()

KEY = os.getenv("MY_JWT_KEY")


def validateAccess(token:str) -> int:
    
    decoded = jwt.decode(token,KEY, algorithms=["HS256"])
    userId = decoded['id']
        
    return userId