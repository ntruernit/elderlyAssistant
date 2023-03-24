import openai
import os
from .utils.config_util import yaml_to_json

configs = yaml_to_json(os.path.dirname(os.path.abspath("API.py")) + "/data/config.yaml")
openai.api_key = configs["OPEN_AI"]


def ask_ai(request):
    ai = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=request["history"]
    )
    answer = ai.choices[0].message.content
    return answer


if __name__ == "__main__":
    ask_ai({
        "history": [
            {
                "role": "system",
                "content": "Du bist der nette Assistent einer älteren Person und du heißt Anna."
            },
            {"role": "assistant", "content": "Wo wohnst du eigentlich?"}
        ]
    })
