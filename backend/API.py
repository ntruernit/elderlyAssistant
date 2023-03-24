import os
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI
import yaml
from fastapi.middleware.cors import CORSMiddleware


from services.utils.greetings import get_greetings
# from services.utils.change_settings import display_settings, detect_request_type
from services import STV, OpenAi
from services.utils.config_util import yaml_to_json, load_json

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
    speech = str(history.dict()["history"][-1]["content"]).lower()
    print(speech)
    configs = yaml_to_json(os.path.dirname(os.path.abspath("API.py")) + "/data/config.yaml")
    print(configs)
    try:
        if ("switch" in speech) or ("talk to" in speech):
            characters = load_json(os.path.abspath("API.py") + "/data/options.json")
            for person, ids in characters.items():
                if person in speech:
                    print(person)
                    configs["DEFAULT_VOICE"] = ids["voice"]
                    configs["DEFAULT_AVATAR"] = ids["avatar"]
                    with open(os.path.dirname(os.path.abspath("API.py")) + "/data/config.yaml", "w") as f:
                        yaml.dump(configs, f)
                    answer = "Hallo, ich bin " + person
                    video = STV.speech_to_video(script=answer)
                    return {"answer": answer, "video": video}
    except Exception as e:
        answer = OpenAi.ask_ai(history.dict())
        video = STV.speech_to_video(script=answer)
        return {"answer": answer, "video": video}
