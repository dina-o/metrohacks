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

#mongodb vars
cluster=MongoClient("mongodb+srv://dina-o:<password>@cluster0.95rgcsy.mongodb.net/?retryWrites=true&w=majority")
db = cluster["metrohacks"]

transactions = db["transactions"]
users = db["transactions"]
db_pending_responses = db['pending_responses']


@app.route("/")
def index():
    return "index is here"

@app.route("/set_spend_limit")
def set_weekly_spend_limit():
    guardian = request.args.get('guardian')
    patient = request.args.get('patient')
    limit = int(request.args.get('limit'))

    patient_record = get_patient_record(patient)
    # checks if the guardian is actually associated with that patient
    if(not patient_record["guardian"] == guardian):
        return Response("{'error': 'not authorized'}", status=403, mimetype='application/json')

    new_spend_limit = { "$set": {"weekly_spend_limit": limit} }
    patient_query = {"username": patient}
    users.update_one(patient_query, new_spend_limit)

    return Response("{\"success\": \"authorize\"}", status=200, mimetype='application/json')

# gets weekly spending limit
@app.route("/get_weekly_limit")
def get_weekly_spend_limit():
    patient = request.args.get('patient')
    spend_limit = get_patient_record(patient)["weekly_spend_limit"]
    formatted_spend_limit = "{:.2f}".format(spend_limit)

    return Response(f"{{\"daily_limit\": {formatted_spend_limit}}}", status=200, mimetype='application/json')

# remaining weekly limit (what patient can presently spend)
@app.route("/get_remaining_weekly_limit")
def get_remaining_weekly_spend_limit():
    patient = request.args.get('patient')
    remaining_spend_limit = get_patient_record(patient)["remaining_spend_limit"]
    formatted_rsl = "{:.2f}".format(remaining_spend_limit)

    return Response(f"{{\"remaining_spend_limit\": {formatted_rsl}}}", status=200, mimetype='application/json')

# gets total balance of patient
@app.route("/get_managed_balance")
def get_managed_balance():
    patient = request.args.get('patient')
    managed_balance = get_patient_record(patient)["managed_account_balance"]
    formatted_mb = "{:.2f}".format(managed_balance)

    return Response(f"{{\"managed_balance\": {formatted_mb}}}", status=200, mimetype='application/json')

# make purchase 
@app.route("/make_purchase")
def make_purchase():
    patient = request.args.get('patient')
    formatted_price = "{:.2f}".format(price) 
    price = float(request.args.get('price'))
    patient_record = get_patient_record(patient)
    guardian_phone_number = patient_record["guardian_phone_number"]
    patient_name = patient_record["full_name"]
    patient_username = patient_record["username"]
    remaining_spend_limit = float(patient_record["remaining_spend_limit"])
    managed_account_balance = float(patient_record["managed_account_balance"])
    if(remaining_spend_limit < price):
        message = twilio_client.messages.create(
            body=f'Authorize ${formatted_price} transaction from {patient_name}?\n\nReply YES to authorize, NO to decline',
            from_=twilio_phone_number,
            to=guardian_phone_number
        )
        if(get_pending_response(guardian_phone_number)):
            delete_pending_response(guardian_phone_number)  #delete record if it's already in userbase

        add_pending_response(guardian_phone_number, price, patient_username, "pending")

        return Response(f"{{\"status\": \"req_auth\", \"remaining_spend_limit\": null, \"managed_balance\": null}}", status=200, mimetype='application/json')

    #patient had enough to spend
    remaining_spend_limit = remaining_spend_limit - price
    managed_account_balance = managed_account_balance - price
    formatted_rsl = "{:.2f}".format(remaining_spend_limit)
    formatted_mab = "{:.2f}".format(managed_account_balance)

    new_limits_and_balance = { "$set": {"remaining_spend_limit": remaining_spend_limit, "managed_account_balance": managed_account_balance} }
    patient_query = {"username": patient}
    users.update_one(patient_query, new_limits_and_balance)
    return Response(f"{{\"status\": \"success\", \"remaining_spend_limit\": {formatted_rsl}, \"managed_balance\": {formatted_mab}}}", status=200, mimetype='application/json')

@app.route("/sms_authorize_response", methods=['GET', 'POST'])
def sms_authorize_payment():

    body = request.values.get('Body', None)
    sender = request.values.get('From', None)

    pending_record = get_pending_response(sender)
    if not pending_record:
        print(f"Nothing pending for {sender}")
        return None

    if pending_record["status"] != "pending":
        print(f"{sender} exists in records but isn't pending")
        return None

    price = float(pending_record["price"])
    formatted_price = "{:.2f}".format(price)

    if body == 'YES':
        update_pending_response_status(sender, "approved")
        # update the patient's financial data
        patient_username = pending_record["patient_username"]
        patient_record = get_patient_record(patient_username)
        managed_account_balance = float(patient_record["managed_account_balance"])
        patient_query = {"username": patient_username}
        new_balance = { "$set": {"managed_account_balance": managed_account_balance - price} }
        users.update_one(patient_query, new_balance)
    elif body == 'NO':
        update_pending_response_status(sender, "declined")
    return

# gets patient record from database
def get_patient_record(patient):
    patient_query = {"username": patient}
    return users.find(patient_query)[0]

def add_pending_response(guardian_phone_number, price, patient_username, status):
    pending_response = {"guardian_phone_number": guardian_phone_number, "price": price, "patient_username": patient_username, "status": status}
    db_pending_responses.insert_one(pending_response)

#get pending response
def get_pending_response(guardian_phone_number):
    pending_response_query = {"guardian_phone_number": guardian_phone_number}
    response = db_pending_responses.find_one(pending_response_query)
    return response

#update pending response status
def update_pending_response_status(guardian_phone_number, status):
    new_status = { "$set": {"status": status} }
    pending_response_query = {"guardian_phone_number": guardian_phone_number}
    db_pending_responses.update_one(pending_response_query, new_status)
    return None

#delete pending response
def delete_pending_response(guardian_phone_number):
    pending_response_query = {"guardian_phone_number": guardian_phone_number}
    db_pending_responses.delete_one(pending_response_query)
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)