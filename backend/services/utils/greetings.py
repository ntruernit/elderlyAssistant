import datetime
import random
from .config_util import load_json
import time


def get_greetings():
    # using now() to get current time
    current_time = datetime.datetime.now()
    # Printing value of now.
    time_ = datetime.datetime.strptime(time.strftime("%H:%M:%S"), '%H:%M:%S').time()
    loaded_json = load_json()
    for times in loaded_json.values():
        start_time = datetime.datetime.strptime(times["start"], '%H:%M:%S').time()
        end_time = datetime.datetime.strptime(times["end"], '%H:%M:%S').time()
        if start_time < time_ < end_time:
            print('entered here at least')
            print(random.choice(times["greetings"]))
            return str(random.choice(times["greetings"]))
