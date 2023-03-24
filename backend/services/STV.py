import requests
import json
import os
from .utils.config_util import yaml_to_json, load_json


def speech_to_video(script):
    configs_ = yaml_to_json(os.path.dirname(os.path.abspath("API.py")) + "/data/config.yaml")
    configs = load_json("/data/defaults.json")
    url = "https://fast-video-api-vktictsuea-nw.a.run.app/api/v1/videos"
    print(configs["DEFAULT_VOICE"])
    payload = {"videoFormat": "mp4", "script": script,
               "voiceId": configs['DEFAULT_VOICE'], "avatarId": configs['DEFAULT_AVATAR']}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Key": configs_["YEPIC"]
    }
    response = requests.post(url, json=payload, headers=headers)
    res = json.loads(response.text)
    return res


if __name__ == "__main__":
    speech_to_video("Hello")
