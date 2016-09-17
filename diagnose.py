import os
import sys
import json

def getResponse(message):
	# gender
	# age
	# 
    if message.get("text"): # get message
        response = message["text"]
        log("THIS IS THE RESPONSE = ",response)
    elif message.get("attachments"):    # get attachment
        attach = message["attachments"][0]  # loop over attachments?
        if attach["type"] == "location":
            latitude = attach["payload"]["coordinates"]["lat"]
            longitude = attach["payload"]["coordinates"]["long"] 
            response = response + "Location: " + str(latitude) + ", " + str(longitude)  
        elif attach["type"] == "image":
            image_url = attach["payload"]["url"]
            response = "Image url: " + image_url
	return response