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
                    response = None

                    # sort different types of messages
                    message = messaging_event["message"]

                    if message.get("text"):
                        response = diagnose.getResponse(message["text"])
                    elif message.get("attachments"):
                        attach = message["attachments"]
                        if attach["payload"]:
                            payload = attach["payload"]
                            if payload.get("coordinates"):
                                coordinates = payload["coordinates"]
                                response = "got location"
                        # get("payload").get("coordinates"):
                        # location = message["attachments"]["title"]
                        # response = diagnose.getResponse(location)



                    # try: #if text
                    #     message_text = messaging_event["message"]["text"]
                    #     response = diagnose.getResponse(message_text)
                    #     break
                    # except:
                    #     pass
                    # try: # if location
                    #     latitude = messaging_event["message"]["attachments"]["payload"]["coordinates"]["lat"]
                    #     longitude = messaging_event["message"]["attachments"]["payload"]["coordinates"]["long"]
                    #     response = "I got a location!"
                    #     # response = "Location is: " + str(latitude) + ", " + str(longitude)
                    #     break
                    # except:
                    #     pass

                    if response is not None:
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


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
