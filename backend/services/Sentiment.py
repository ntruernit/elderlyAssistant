from transformers import pipeline

def classify_sentiment(text:str):
    pipe = pipeline("text-classification")
    res = pipe(text)
    print(res)
    return res