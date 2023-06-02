#!/usr/bin/env python

import os
import re

from dotenv import load_dotenv
from faker import Faker
from flask import Flask, Response, jsonify, redirect, request
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import Dial, VoiceResponse

load_dotenv()
print("TWILIO_ACCOUNT_SID:", os.getenv("TWILIO_ACCOUNT_SID"))
print("TWILIO_CALLER_ID:", os.getenv("TWILIO_CALLER_ID"))
print("TWILIO_TWIML_APP_SID:", os.getenv("TWILIO_TWIML_APP_SID"))
print("API_KEY:", os.getenv("API_KEY"))
print("API_SECRET:", os.getenv("API_SECRET"))


app = Flask(__name__)
fake = Faker()
alphanumeric_only = re.compile("[\W_]+")
phone_pattern = re.compile(r"^[\d\+\-\(\) ]+$")

twilio_number = os.environ.get("TWILIO_CALLER_ID")

# Store the most recently created identity in memory for routing calls
IDENTITY = {"identity": ""}


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/token", methods=["GET"])
def token():
    # get credentials for environment variables
    account_sid = os.environ.get("AC9abd4a54209c7da2081f881c918ff591")
    application_sid = os.environ.get("AP62aa6ce1a53f6fd53236c9fd955ed648")
    api_key = os.environ.get("SK3b4261cb982b38c11ed9090b80dab1a6")
    api_secret = os.environ.get("YcsujrT2TfFb7xwl5wF8oU8DcAOJ8FYz")

    # Generate a random user name and store it
    identity = alphanumeric_only.sub("", fake.user_name())
    IDENTITY["identity"] = identity

    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a Voice grant and add to token
    voice_grant = VoiceGrant(
        outgoing_application_sid=application_sid,
        incoming_allow=True,
    )
    token.add_grant(voice_grant)

    # Return token info as JSON
    token = token.to_jwt()

    # Return token info as JSON
    return jsonify(identity=identity, token=token)


@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    if request.form.get("To") == twilio_number:
        # Receiving an incoming call to our Twilio number
        dial = Dial()
        # Route to the most recently created client based on the identity stored in the session
        dial.client(IDENTITY["identity"])
        resp.append(dial)
    elif request.form.get("To"):
        # Placing an outbound call from the Twilio client
        dial = Dial(caller_id=twilio_number)
        # wrap the phone number or client name in the appropriate TwiML verb
        # by checking if the number given has only digits and format symbols
        if phone_pattern.match(request.form["To"]):
            dial.number(request.form["To"])
        else:
            dial.client(request.form["To"])
        resp.append(dial)
    else:
        resp.say("Thanks for calling!")

    return Response(str(resp), mimetype="text/xml")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
