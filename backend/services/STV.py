import requests
import json
import os


def speech_to_video(script):
    url = "https://fast-video-api-vktictsuea-nw.a.run.app/api/v1/videos"
    payload = {"videoFormat": "mp4", "script": script,
               "voiceId": os.environ['DEFAULT_VOICE'], "avatarId": os.environ['DEFAULT_AVATAR']}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Key": os.environ["YEPIC"]
    }
    response = requests.post(url, json=payload, headers=headers)
    res = json.loads(response.text)
    return res


if __name__ == "__main__":
    speech_to_video("Hello")
