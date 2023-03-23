from fastapi import FastAPI
from pydantic import BaseModel
from STT import speech_to_text
from OpenAi import Assistant
from TTS import text_to_speech

class Question(BaseModel):
    question: str


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/stt/")
def convert_speech_text(filepath: str):
    return speech_to_text(filepath)

@app.post("/get_answer/")
def get_answer(question: Question):
    assistant = Assistant()
    return assistant.askQuestion(question.question)

@app.post("/tts/")
def get_speech(question: Question):
    text_to_speech(question.question)






