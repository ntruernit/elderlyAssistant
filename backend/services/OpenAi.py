import openai, os, pickle
from .TTS import speech_to_video
openai.api_key = "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"


class Assistant():
    def __init__(self):
        self.history = [{'role': 'system',
                         'content': 'Du bist der nette Assistent einer älteren Person.'}]

    def askQuestion(self, question):
        self.history.append({
            "role": "user",
            "content": question
        })
        ai = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.history
        )
        self.history.append({
            "role": "assistant",
            "content": ai.choices[0].message.content
        })
        print(ai.choices[0].message.content)
        speech_to_video(script=ai.choices[0].message.content)
        return ai.choices[0].message.content

    def printConversation(self):
        for row in self.history[1:]:
            print(row["role"], ":", row["content"])

    def loop(self):
        print("type exit to leave or")
        question = ""
        while question != "exit":
            question = input("// enter your question \n: ")
            self.askQuestion(question)
            os.system('clear')
            self.printConversation()


if __name__ == "__main__":
    a = Assistant()
    # print(a.askQuestion("Where is India?"))
    a.loop()
