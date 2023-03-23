from fastapi import FastAPI
from pydantic import BaseModel
from services.STT import speech_to_text
from services.OpenAi import Assistant
from services.TTS import speech_to_video

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
    speech_to_video(script=Question.question)
    speech_to_video(question.question)






