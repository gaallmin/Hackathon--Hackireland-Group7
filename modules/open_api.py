from pydantic import BaseModel
from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv
import os

load_dotenv()

class Pointer(BaseModel):
    subtext: str
    advice: str
    reflection: str

def getPointer(user_subtext=None):
    # API Key in .env file
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    # Current working directory
    CWD = os.getcwd()

    # Conversation data filepath
    CONVO_FILEPATH = os.path.join(CWD, "convo_data.csv")

    client = OpenAI(api_key=OPENAI_API_KEY)

    data = pd.read_csv(CONVO_FILEPATH)

    # Base prompt with conversation history
    prompt = (
        f"I'm in the middle of a conversation with someone, some of their previous statements in table format are: {data}.\n"
        f"The latest statement is the last line in the sheet."
    )
    
    # If a new user subtext is provided, include it in the prompt.
    if user_subtext:
        prompt += f" The user's new subtext is: {user_subtext}.\n"
    
    prompt += (
        " Considering the associated emotion and confidence level, give a maximum of 50 characters on any subtext being conveyed "
        "and 50 more characters on any advice you would give on how to act in this situation, finally give 150 characters on "
        "things to reflect on after the conversation is over. Provide full context for this."
    )

    pointer = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user", 
                "content": prompt
            }
        ],
        response_format=Pointer,
    )

    return pointer
