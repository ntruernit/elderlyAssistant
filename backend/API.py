from typing import List
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from services.utils.greetings import get_greetings
from services import STV, OpenAi

class HistoryItem(BaseModel):
    role: str
    content: str


class HistoryRequest(BaseModel):
    history: List[HistoryItem]


app = FastAPI()


@app.get("/")
def read_root():
    message_1 = get_greetings()
    print(message_1)
    return message_1
    # return {"Hello": "World"}


@app.post("/process_input")
def get_answer(history: HistoryRequest):
    answer = OpenAi.ask_ai(history.dict())
    video = STV.speech_to_video(script=answer)
    return {"answer": answer, "video": video}
