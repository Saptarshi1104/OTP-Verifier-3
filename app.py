import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from twilio.rest import Client

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def verify_otp():
    username = request.form['username']
    password = request.form['password']
    mobile_number = request.form['number']
    if username == 'verify' and password == '12345':   
        account_sid = 'AC63a912284e734e7648f9efcc4c67e984'
        auth_token = '60475415d39354ae95fbe64acdeb2202'
        client = Client(account_sid, auth_token)
        verification = client.verify \
            .services('VAe5a9d5a15419befb80e10605a6918703') \
            .verifications \
            .create(to=mobile_number, channel='sms')
        print(verification.status)
        return render_template("otp_verify.html")
    else:
        return render_template('user_error.html')

@app.route('/otp', methods=['POST'])
def get_otp():
    print("Processing")
    received_otp = request.form['received_otp']
    mobile_number = request.form['number']
    account_sid = 'AC63a912284e734e7648f9efcc4c67e984'
    auth_token = '60475415d39354ae95fbe64acdeb2202'
    client = Client(account_sid, auth_token)
    verification_check = client.verify \
        .services('VAe5a9d5a15419befb80e10605a6918703') \
        .verification_checks \
        .create(to=mobile_number, code=received_otp)
    print(verification_check.status)
    if verification_check.status == 'pending':
        return "Entered OTP is wrong"
    else:
        return redirect("https://collaborative-document-up5u.onrender.com")
    
if __name__ == "__main__":
    app.run()