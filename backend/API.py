from fastapi import FastAPI
from pydantic import BaseModel

from services import STT, TTS, OpenAi
from services.utils.greetings import get_greetings


class Question(BaseModel):
    question: str


app = FastAPI()


@app.get("/")
def read_root():
    message_1 = get_greetings()
    print(message_1)
    return message_1
    # return {"Hello": "World"}


@app.post("/stt/")
def convert_speech_text(filepath: str):
    return STT.speech_to_text()


@app.post("/get_answer/")
def get_answer(question:Question):
    assistant = OpenAi.Assistant()
    return assistant.askQuestion(question.question)

@app.post("/tts/")
def get_speech(question:Question):
    TTS.text_to_speech(question.question)







