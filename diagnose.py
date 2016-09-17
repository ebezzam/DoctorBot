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



