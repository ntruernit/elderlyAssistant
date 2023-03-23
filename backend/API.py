from fastapi import FastAPI
from pydantic import BaseModel

from services import STT, TTS, OpenAi
from backend.utils_.greetings import get_greetings


class Question(BaseModel):
    question: str


app = FastAPI()

@app.get("/")
def read_root():
    return get_greetings()
    # return {"Hello": "World"}

@app.post("/stt/")
def convert_speech_text(filepath: str):
    return STT.speech_to_text(filepath)


@app.post("/get_answer/")
def get_answer(question:Question):
    assistant = OpenAi.Assistant()
    return assistant.askQuestion(question.question)


@app.post("/tts/")
def get_speech(question:Question):
    TTS.text_to_speech(question.question)







