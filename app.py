import os
import sys
import json

import requests
import diagnose
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

                    # sort different types of messages
                    response = None
                    message = messaging_event["message"]
                    if message.get("text"): # get message
                        message = message["text"]
                    elif message.get("attachments"):    # get attachment
                        attach = message["attachments"][0]  # loop over attachments?
                        if attach["type"] == "location":
                            latitude = attach["payload"]["coordinates"]["lat"]
                            longitude = attach["payload"]["coordinates"]["long"] 
                            message = "Location: " + str(latitude) + ", " + str(longitude)  
                        elif attach["type"] == "image":
                            image_url = attach["payload"]["url"]
                            message = "Image url: " + image_url
                    response = diagnose.get_response(message)                               

                    if response is not None:
                        log(response)
                        if response == "Hi":
                            init_buttom_template(sender_id)
                        else:
                            send_message(sender_id, response)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def init_buttom_template(recipient_id):

    log("Sending button template to {recipient}.".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"Hey! How can I help you?",
                    "buttons":[
                        {
                        'type': 'postback',
                        'title': 'Use Symptom Checker',
                        'payload': 'symptomChecker_init'
                        },
                        {
                        'type': 'postback',
                        'title': 'View Health Alerts near you',
                        'payload': 'healtAlerts_init'
                        },
                        {
                        'type': 'postback',
                        'title': 'Get some Medical Information',
                        'payload': 'medInfo_init'
                        }
                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
