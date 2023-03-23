from typing import Union

from fastapi import FastAPI
from STT import speech_to_text


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/stt/")
def convert_speech_text(filepath: str):
    return speech_to_text(filepath)




