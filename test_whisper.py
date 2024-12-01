import re
import whisper_timestamped as whisper
from jinja2 import Environment, FileSystemLoader
from string import punctuation
import argparse


keywords = ("mist","sitrep","9 liner", "nine liner", "contact report", "radio check")

parser = argparse.ArgumentParser("test_whisper")
parser.add_argument("filePath", help="The Path to audio file to be used with program")
args = parser.parse_args()
# TODO if running through gui load audio wont be this file
# should make this accept a filename instead of hardcoded
filePath = args.filePath
audio = whisper.load_audio(filePath)

model = whisper.load_model("turbo", device="cpu")

result = whisper.transcribe(model, audio, language="en")


modelText = result["text"]


modelTextLower = modelText.lower()

index = modelTextLower.rindex("out")
modelText = modelText[:index]


splitModelText = re.split('[.?]',modelText)

### Helper Methods 
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
        end_index = find_after_index(arr,end_str, start_index) 
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

def extract_between_strings(text, start_substr, end_substr): 
    start_index = text.find(start_substr) 
    if start_index != -1: 
        start_index += len(start_substr) # Move start_index to the end of start_substr 
        end_index = text.find(end_substr, start_index) 
        if end_index != -1: 
            return text[start_index:end_index] 
    return 'N/A'


def filter_sentence(text):
    if(text.find("more to follow")!= -1):
        index = text.index("more to follow")
        # also remove any punctuation if it's the first char
        updatedText = text[:index-1]
        updatedText.lstrip(punctuation)
        return updatedText
    else:
        return text 

#### methods for generating the corresponding file format  
### should be updated to detect a range of keywords for each report 

if modelTextLower.find('sit rep') != -1:
    textSegments = re.split(" ",modelTextLower)
    callsign1 = textSegments[find_adjacent_index(textSegments,"this","is",True)]
    callsign2 = textSegments[find_adjacent_index(textSegments,"this","is",False)]
    enemy = filter_sentence(concatenate_between_strings(textSegments,'alpha','bravo'))
    friendly = filter_sentence(concatenate_between_strings(textSegments,'bravo','charlie'))
    admin = filter_sentence(concatenate_between_strings(textSegments,'charlie','para'))
    other = filter_sentence(concatenate_between_strings(textSegments,'delta','over'))

    environment = Environment(loader=FileSystemLoader("templates/"))
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


if modelTextLower.find('contact report') != -1:
    textSegments = re.split(" ",modelTextLower)
    callsign1 = textSegments[find_adjacent_index(textSegments,"this","is",True)]
    callsign2 = textSegments[find_adjacent_index(textSegments,"this","is",False)]
    contactTime = extract_between_strings(modelTextLower,'time of contact','enemy location')
    enemyLocation = extract_between_strings(modelTextLower,'enemy location','observer location')
    observerLocation = extract_between_strings(modelTextLower,'observer location','description of target')
    targetDescription = extract_between_strings(modelTextLower,'description of target','enemy action')
    enemyAction = extract_between_strings(modelTextLower,'enemy action','own action') 
    ownAction = extract_between_strings(modelTextLower,'own action','over')

    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("contactReport.txt")
    data = {
        "callsign1":callsign1,
        "callsign2":callsign2,
        "contactTime":contactTime,
        "enemyLocation":enemyLocation,
        "observerLocation":observerLocation,
        "targetDescription":targetDescription,
        "enemyAction":enemyAction,
        "ownAction":ownAction
    }
    content = template.render(
        data
    )

    print(content)

    filename = "contactReportResult.txt"


    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print("generating report from audio complete")
    

if modelTextLower.find('mist report') != -1:
   callsign1 = textSegments[find_adjacent_index(textSegments,"this","is",True)]
   callsign2 = textSegments[find_adjacent_index(textSegments,"this","is",False)]
   mechanism = extract_between_strings(modelTextLower,'mechanism','injury description')
   injury = extract_between_strings(modelTextLower,'injury description','status')
   status = extract_between_strings(modelTextLower,'status','treatment')
   treatment = extract_between_strings(modelTextLower,'treatment','over')
   
   environment = Environment(loader=FileSystemLoader("templates/"))
   template = environment.get_template("mist_report.txt")
   data = {
        "callsign1":callsign1,
        "callsign2":callsign2,
        "mechanism":mechanism,
        "injury":injury,
        "status_symptoms":status,
        "treatment":treatment
    }
   
   content = template.render(
        data
   )

   print(content)

   filename = "mistReportResult.txt"


   with open(filename, mode="w", encoding="utf-8") as message:
       message.write(content)
       print("generating report from audio complete")

   




