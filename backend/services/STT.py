from transformers import pipeline

def speech_to_text(filepath:str):
    cls = pipeline("automatic-speech-recognition")

    res = cls("/Users/prasun/Downloads/Hackathons/StartHack-23/elderlyAssistant/harvard.wav")

    # print(res)
    return res