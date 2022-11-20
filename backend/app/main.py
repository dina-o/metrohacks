from flask import Flask, Response, request
from flask_cors import CORS
from twilio.rest import Client
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

#twilio set up
twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID'] 
twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_client = Client(twilio_account_sid, twilio_auth_token)
twilio_phone_number = '+19896569349'
# Phone numbers who we are expecting responses from
waiting_phone_numbers = []

cluster=MongoClient("mongodb+srv://dina-o:<password>@cluster0.95rgcsy.mongodb.net/?retryWrites=true&w=majority")
db = cluster["metrohacks"]

transactions = db["transactions"]
users = db["transactions"]
awaiting_responses = db["awaiting_resp"]


@app.route("/")
def index():
    return "index is here"

@app.route("/set_spend_limit")
def set_daily_spend_limit():
    guardian = request.args.get('guardian')
    patient = request.args.get('patient')
    limit = int(request.args.get('limit'))

    patient_record = get_patient_record(patient)
    # checks if the guardian is actually associated with that patient
    if(not patient_record["guardian"] == guardian):
        return Response("{'error', 'not authorized'}", status=403, mimetype='application/json')

    new_spend_limit = { "$set": {"weekly_spend_limit": limit} }
    patient_query = {"username": patient}
    users.update_one(patient_query, new_spend_limit)

    return Response("{'success', 'authorized'}", status=200, mimetype='application/json')

# gets weekly spending limit
@app.route("/get_weekly_limit")
def get_weekly_spend_limit():
    patient = request.args.get('patient')
    spend_limit = get_patient_record(patient)["weekly_spend_limit"]

    return Response(f"{{'weekly_limit', '{spend_limit}'}}", status=200, mimetype='application/json')

# gets total balance of patient
@app.route("/get_managed_balance")
def get_managed_balance():
    patient = request.args.get('patient')
    managed_balance = get_patient_record(patient)["managed_account_balance"]

    return Response(f"{{'managed_balance', '{managed_balance}'}}", status=200, mimetype='application/json')

# gets patient record from database
def get_patient_record(patient):
    patient = request.args.get('patient')
    patient_query = {"username": patient}
    return users.find(patient_query)[0]

def message(guardian_phone_number):
    message = twilio_client.messages.create(
        to=guardian_phone_number,
        from_=twilio_phone_number,
        body='Authorize ${price} transaction from {patient_name}? \n\nReply YES to authorize, NO to decline' )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)