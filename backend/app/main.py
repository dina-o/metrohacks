from flask import Flask, Response, request
from twilio.rest import Client
import os

app = Flask(__name__)

#twilio set up
twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID'] 
twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_client = Client(twilio_account_sid, twilio_auth_token)
twilio_phone_number = '+19896569349'
#other vars
price = "$230"
patient_name = "Sally"
# Phone numbers who we are expecting responses from
waiting_phone_numbers = []

@app.route("/")
def index():
    return "index is here"

def message(guardian_phone_number):
    message = twilio_client.messages.create(
        to=guardian_phone_number,
        from_=twilio_phone_number,
        body='Authorize ${price} transaction from {patient_name}? Location: (insert location)\n\nReply YES to authorize, NO to decline' )



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)