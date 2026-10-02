from fastapi import APIRouter
import os
from dotenv import load_dotenv

load_dotenv()

base_router = APIRouter(
    tags=["Base"],

)

@base_router.get("/")
def welcome():
    app_name = os.getenv("APP_NAME")
    return {
        "message": "Welcome to the Application Contract Overview API!",
        "app_name": app_name,
    } 