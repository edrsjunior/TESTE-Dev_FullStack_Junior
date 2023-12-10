from dotenv import load_dotenv
import os

load_dotenv()

KEY = os.getenv("MY_JWT_KEY")
print(KEY)

def verifyJWTToken(token: str):
    
    return