import re
import whisper_timestamped as whisper
from jinja2 import Environment, FileSystemLoader

keywords = ("mist","sitrep","9 liner", "nine liner", "contact report", "radio check")

audio = whisper.load_audio("Sitrep.mp3")

model = whisper.load_model("turbo", device="cpu")

result = whisper.transcribe(model, audio, language="en")

#import json
#print(json.dumps(result, indent = 2, ensure_ascii = False))
#print(result["text"])

modelText = result["text"]
index = modelText.find("out")
modelText = modelText[:index]
modelTextLower = modelText.lower()

splitModelText = re.split('[.?]',modelText)
print(splitModelText)

def find_adjacent_index(arr, str1, str2, after): 
    for i in range(len(arr) - 1): 
        if arr[i] == str1 and arr[i + 1] == str2: 
            if after:
                return i + 2
            else:
                return i-1  
    return -1

def concatenate_between_strings(arr, start_str, end_str): 
    try: 
        start_index = arr.index(start_str) + 1 
        end_index = find_after_index(arr,end_str, start_index)#arr.find(end_str,start_index) 
        if start_index < end_index: 
            return ' '.join(arr[start_index:end_index]) 
        else: return 'N/A' # Return an empty string if the start index is after the end index 
    except ValueError: 
        return 'N/A'
    
def find_after_index(strings, target, start_index): 
    for i in range(start_index, len(strings)): 
        if strings[i] == target: 
            return i 
    return -1

#if any('sit rep' in modelTextLower): 
if modelTextLower.find('sit rep') != -1:
    textSegments = re.split(" ",modelTextLower)
    print(textSegments)
    callsign1 = textSegments[find_adjacent_index(textSegments,"this","is",True)]
    print(callsign1)
    callsign2 = textSegments[find_adjacent_index(textSegments,"this","is",False)]
    print(callsign2)
    enemy = concatenate_between_strings(textSegments,'alpha','bravo')
    print(enemy)
    friendly = concatenate_between_strings(textSegments,'bravo','charlie')
    print(friendly)
    admin = concatenate_between_strings(textSegments,'charlie','delta')
    print(admin)
    other = concatenate_between_strings(textSegments,'delta','over')
    print(other)

    environment = Environment(loader=FileSystemLoader("."))
    template = environment.get_template("sitrep.txt")
    data = {
        "callsign1":callsign1,
        "callsign2":callsign2,
        "enemy":enemy,
        "friendly":friendly,
        "admin":admin,
        "other":other
    }
    content = template.render(
        data
    )

    print(content)

    filename = "sitrepResult.txt"


    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print("generating report from audio complete")






