from llama_index.core.tools import FunctionTool
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from bson import ObjectId
from datetime import datetime
import requests

load_dotenv()

uri = os.getenv("MONGODB_URI")
weather_api_key = os.getenv("OPEN_WEATHER_API_KEY")

client = MongoClient(uri, server_api=ServerApi("1"))
db = client["user_database"]


def get_user_personal_data():
    try:
        users_collection = db["users"]
        user_id = ObjectId(os.getenv("USER_ID"))
        user_data = users_collection.find_one({"_id": user_id})
        return user_data
    except Exception as e:
        print(f"Error: {e}")


def get_user_notes():
    try:
        notes_collection = db["notes"]
        return list(notes_collection.find({}))
    except Exception as e:
        print(f"Error: {e}")


def add_note_to_user(note):
    try:
        notes_collection = db["notes"]
        user_id = ObjectId(os.getenv("USER_ID"))
        return notes_collection.insert_one({"user_id": user_id, "note": note})
    except Exception as e:
        print(f"Error: {e}")


def get_date_and_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Location hardcoded
def get_current_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat=44.6488&lon=-63.5752&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return f"Weather: {data['weather'][0]['description']}, Temperature: {int(data['main']['temp'])}°C, Wind Speed: {int(data['wind']['speed'])} m/s"
    except requests.RequestException as e:
        print(f"Request error: {e}")


note_engine = FunctionTool.from_defaults(
    fn=add_note_to_user,
    name="note_adder",
    description="This tool saves a note as a string to the user's data document. This tool is not for answering questions.",
)

get_user_personal_data_engine = FunctionTool.from_defaults(
    fn=get_user_personal_data,
    name="user_personal_data",
    description="Do not use this tool if you don't need user's personal information. This tool returns user's personal information except his resume. This tool doesn't provide any other functionality. Do not use this tool if you need user's resume, education, skills and work experience.",
)

get_user_notes_engine = FunctionTool.from_defaults(
    fn=get_user_notes,
    name="user_notes",
    description="Do not use this tool if you don't need user's notes. This tool returns user's notes. This tool doesn't provide any other functionality.",
)

get_date_and_time_engine = FunctionTool.from_defaults(
    fn=get_date_and_time,
    name="date_and_time",
    description="Do not use this tool if you don't need date and time. This tool returns current date and time. This tool doesn't provide any other functionality.",
)

get_current_weather_engine = FunctionTool.from_defaults(
    fn=get_current_weather,
    name="current_weather",
    description="Do not use this tool if you don't need current weather. This tool returns current weather. This tool doesn't provide any other functionality.",
)
