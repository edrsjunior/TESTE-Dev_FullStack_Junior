import datetime
from dotenv import load_dotenv
import os
from fastapi import HTTPException

import jwt

load_dotenv()

KEY = os.getenv("MY_JWT_KEY")

def validateAccess(token:str) -> int:
    try:
        decoded = jwt.decode(token,KEY, algorithms=["HS256"])
        userId = decoded['id']
        
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(
            status_code= 498,
            detail="Invalid Token"
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
        status_code= 498,
        detail="Expired Token"
        )
    return userId