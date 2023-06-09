import os
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.utils.greetings import get_greetings
from services import STV, OpenAi

class HistoryItem(BaseModel):
    role: str
    content: str


class HistoryRequest(BaseModel):
    history: List[HistoryItem]


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    answer = get_greetings()
    video = STV.speech_to_video(script=answer)
    return {"answer": answer, "video": video}


@app.post("/process_input")
def get_answer(history: HistoryRequest):
    answer = OpenAi.ask_ai(history.dict())
    video = STV.speech_to_video(script=answer)
    return {"answer": answer, "video": video}
