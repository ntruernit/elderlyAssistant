import os
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI
# from dotenv import load_dotenv
# load_dotenv()

from services.utils.greetings import get_greetings
from services.utils.change_settings import display_settings, detect_request_type
from services import STV, OpenAi
from services.utils.config_util import yaml_to_json

class HistoryItem(BaseModel):
    role: str
    content: str


class HistoryRequest(BaseModel):
    history: List[HistoryItem]


app = FastAPI()


@app.get("/")
def read_root():
    answer = get_greetings()
    video = STV.speech_to_video(script=answer)
    return {"answer": answer, "video": video}


@app.post("/process_input")
def get_answer(history: HistoryRequest):
    configs = yaml_to_json(os.path.dirname(os.path.abspath("API.py")) + "/data/config.yaml")
    if detect_request_type(history.dict()) == 2:
        if configs["REQUEST_TYPE"] == 2:
            answer = "Okay, I will show you a set of avatars, please select your favourite"
            video = STV.speech_to_video(script=answer)
        for num, item in enumerate(display_settings()):
            video = STV.speech_to_video(script="Das is Stimmhaftigkeit " + str(num))
            yield {"video": video}
    else:
        answer = OpenAi.ask_ai(history.dict())
        video = STV.speech_to_video(script=answer)
        return {"answer": answer, "video": video}
