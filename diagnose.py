import os
import sys
import json

def get_response(message):
	# gender
	# age
	# 
    response = None
    if message[0].get("text"): # get message
        response = message["text"]
    elif message.get("attachments"):    # get attachment
        attach = message["attachments"][0]  # loop over attachments?
        if attach["type"] == "location":
            latitude = attach["payload"]["coordinates"]["lat"]
            longitude = attach["payload"]["coordinates"]["long"] 
            response = "Location: " + str(latitude) + ", " + str(longitude)  
        elif attach["type"] == "image":
            image_url = attach["payload"]["url"]
            response = "Image url: " + image_url
	return response