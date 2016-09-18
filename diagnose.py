import os
import sys
import json
import requests
import urllib, json
import infermedica_api
api = infermedica_api.API(app_id='21794b8d', app_key='81f5f69f0cc9d2defaa3c722c0e905bf')
print(api.info())

def gender(sender_id):

    # get user info
    r = requests.get('https://graph.facebook.com/v2.6/'+sender_id+
        '?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token='+os.environ["PAGE_ACCESS_TOKEN"])
    try:
        gender = str(r.json()["gender"])
    except:
        gender = ""


def searchSymptom(symptom, sender_id):
	if symptom == "fever":
		return "s_98"
	if symptom == "headache":
		return "s_21"
	if symptom == "knee pain":
		return "s_581"


def init_diagnose(symptom_id,age,gender,sender_id):
	request = infermedica_api.Diagnosis(sex=gender, age=age)
	request.add_symptom(symptom_id, 'present')
	request = api.diagnosis(request)
	return request

def improve_diagnosis(request,sender_id,question_id,choice_id):
	request.add_symptom(question_id,choice_id)
	request = api.diagnosis(request)
	return request


x = init_diagnose("s_581",22,"male",22)
# question = str(x.question.text)

# x.add_symptom("s_21",'present')
# request = api.diagnosis(x)
# print request
