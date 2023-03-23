from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
import requests
from ..utils.config_util import yaml_to_json
# from config import DEFAULT_AVATAR, DEFAULT_VOICE


# def text_to_speech(text_to_convert:str):
#     processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
#     model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
#     vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
#
#     inputs = processor(text=text_to_convert, return_tensors="pt")
#
#     # load xvector containing speaker's voice characteristics from a dataset
#     embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
#     speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
#
#     speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
#
#     sf.write("speech.wav", speech.numpy(), samplerate=16000)


def speech_to_video(script):
    configs = yaml_to_json('config.yaml')
    url = "https://fast-video-api-vktictsuea-nw.a.run.app/api/v1/videos"
    payload = {"videoFormat": "mp4", "script": script,
               "voiceId": configs['DEFAULT_VOICE'], "avatarId": configs['DEFAULT_AVATAR']}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Key": "509cf5af-1e3f-4a81-8589-6f36e0e1eb57"
    }
    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


if __name__ == "__main__":
    speech_to_video()