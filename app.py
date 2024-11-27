from llama_index.core.tools import FunctionTool
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from user_engines import (
    note_engine,
    get_user_personal_data_engine,
    get_user_notes_engine,
    get_date_and_time_engine,
    get_current_weather_engine,
)
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI

load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["user_database"]
conversation_collection = db["conversation_history"]
conversation_history = []
# Honorific hardcoded
context = """You are a helpful assistant named 'Jarvy'. Provide information in a formal and supportive manner. Current language is English, always use English. Keep your responses concise and to the point. Use the word 'sir' whenever you can."""


def serialize_response(response):
    return str(response)


def add_to_conversation(role, content):
    conversation_history.append(
        {"role": role, "content": content, "timestamp": datetime.now().isoformat()}
    )


def save_conversation_history():
    if conversation_history:
        conversation_collection.insert_one({"messages": conversation_history})
        print("Conversation history saved to database.")
    else:
        print("No conversation history to save.")


def restart_conversation():
    save_conversation_history()
    conversation_history.clear()
    print("Conversation restarted.")


restart_conversation_engine = FunctionTool.from_defaults(
    fn=restart_conversation,
    name="restart_conversation",
    description="This tool restarts the conversation and saves the history to the database.",
)


app = Flask(__name__)
CORS(app)

tools = [
    note_engine,
    get_user_personal_data_engine,
    restart_conversation_engine,
    get_user_notes_engine,
    get_date_and_time_engine,
    get_current_weather_engine,
]

llm = OpenAI(model="gpt-4o-mini")
agent = ReActAgent.from_tools(
    tools, llm=llm, max_iterations=10, verbose=True, context=context
)


@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    prompt = data.get("prompt", "")

    add_to_conversation("user", prompt)

    response = agent.query(
        "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    )

    assistant_response = serialize_response(response)
    add_to_conversation("assistant", assistant_response)

    return jsonify({"response": assistant_response})


@app.route("/conversation_history", methods=["GET"])
def conversation():
    print("Conversation history retrieved.")
    return jsonify({"conversation_history": conversation_history})


if __name__ == "__main__":
    app.run(debug=True)
