import datetime


def get_greetings():
    # using now() to get current time
    current_time = datetime.datetime.now()
    # Printing value of now.
    print("Current_time is ", current_time)
    time = current_time.strftime("%H:%M:%S")
    print("time:", time)
    return "Hello"