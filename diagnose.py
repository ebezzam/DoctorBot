import os
import sys
import json
import requests

def diagnose(sender_id):

    # get user info
    r = requests.get('https://graph.facebook.com/v2.6/'+sender_id+
        '?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token='+os.environ["PAGE_ACCESS_TOKEN"])
    try:
        gender = str(r.json()["gender"])
    except:
        gender = ""




def apiai_symptom(message):

    CLIENT_ACCESS_TOKEN = 'f2c3166a316843ca95e399a19333c873'
    ai = apiai.ApiAI('31df623f4c1846209c287dc9e8f36a2e')

    request = ai.text_request()

    request.lang = 'en'  # optional, default value equal 'en'

    # request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    request.query = message
    response = request.getresponse()
    data = json.loads(response.read())
    response = str(data["result"]["fulfillment"]["speech"])
    symptom = str(data["result"]["parameter"]["symptoms"])
    return symptom

