from config_util import load_json
from ..STV import speech_to_video

# check that the work settings was said and send request to here
def display_settings(category="voices"):
    loaded_data = load_json("/data/options.json")
    return loaded_data[category]
    # for num, item in enumerate(loaded_data[category]):
    #     output.append(speech_to_video("Das is Stimmhaftigkeit " + num))
    #     yield


def detect_request_type(request):
    if "settings" in request["history"][].lower() and "change" in request["history"][].lower():
        return 2
    else:
        return 1


#js function
# if (text.includes("settings") && text.includes("change")) {
# 	console.log("These words are there, activate change settings");
#     change state to settings
# }