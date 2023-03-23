from transformers import pipeline

def speech_to_text(filepath:str = None):
    cls = pipeline("automatic-speech-recognition")

    res = cls(filepath)

    print(res)
    return res

# speech_to_text("/Users/prasun/Downloads/Hackathons/StartHack-23/elderlyAssistant/backend/data/harvard.wav")