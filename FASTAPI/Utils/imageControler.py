import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_NAME"), 
  api_key = os.getenv("CLOUDINARY_API"),
  api_secret = os.getenv("CLOUDINARY_SECRET"),
)

async def uploadImg(image:UploadFile, userFolder: int,) -> str:
    
  response = cloudinary.uploader.upload(
    image, 
    width = 600,
    crop = "limit",
    folder = f'carros/{userFolder}/',
    overwrite = True,
    )

  return response

async def deleteImg(idPost: str):
  try:
    cloudinary.api.delete_resources_by_prefix(idPost)
  except:
    raise Exception("Vailed to delete image")
  