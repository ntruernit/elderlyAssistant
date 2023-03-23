from transformers import pipeline

def speech_to_text(filepath:str = None):
    cls = pipeline("automatic-speech-recognition")

    res = cls("../data/harvard.wav")

    print(res)
    return res