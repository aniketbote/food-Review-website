from flask import Flask, render_template, request, session, jsonify, flash
from firebase import firebase
import pyrebase
import hashlib
import os
import time
import cv2
import numpy as np
import pandas as pd

review_data = pd.read_csv('new.csv')


app = Flask(__name__)
#configuration for firebase
CONFIG = {
    "apiKey": "AIzaSyCs1J_PXXG3HEs1B19YVN7Z-d3JESrui3E",
    "authDomain": "firebird-7ef02.firebaseapp.com",
    "databaseURL": "https://firebird-7ef02.firebaseio.com",
    "projectId": "firebird-7ef02",
    "storageBucket": "firebird-7ef02.appspot.com",
    "messagingSenderId": "574864460908",
    "appId": "1:574864460908:web:c317c3217ae1fcd4899c49",
    "measurementId": "G-15LBYQ506Y"
}



##------------------------------------------------------------------------------##
##__________________________utility functions______________________

def get_data(pro):
    hotels = []
    data_subset = review_data[review_data['province'] == pro]
    for name in list(set(data_subset['name'])):
        print(name)
        hdict = {}
        hotel_subset = data_subset[data_subset['name'] == name]
        hdict['name'] = name
        hdict['reviews'] = list(hotel_subset['reviews.text'])
        hdict['review_user'] = list(hotel_subset['reviews.username'])
        hdict['rating'] = list(hotel_subset['reviews.rating'])
        hdict['city'] = list(hotel_subset['city'])[0]
        hdict['category'] = list(hotel_subset['categories'])[0]
        hdict['address'] = list(hotel_subset['address'])[0]
        hotels.append(hdict)
    return hotels

def logincheck(u_email, u_pass):
    fb_pyre = pyrebase.initialize_app(CONFIG)
    auth = fb_pyre.auth()
    try:
        signin = auth.sign_in_with_email_and_password(u_email, u_pass)
    except Exception as e:
        return False
    return True

def signupcheck(u_dict):
    fb = firebase.FirebaseApplication('https://firebird-7ef02.firebaseio.com/')
    email = u_dict['email']
    res = hashlib.sha256(email.encode())
    sha_email = res.hexdigest()
    result = fb.get('/{}'.format(sha_email), None)
    if result != None:
        valid = False
        msg = 'Email already exists'
        return valid, msg
    else:
        valid = True
        msg = 'Succesfully created profile'
        return valid, msg

def update_db(user_dict):
    fb = firebase.FirebaseApplication('https://firebird-7ef02.firebaseio.com//')
    fb_pyre = pyrebase.initialize_app(CONFIG)
    auth = fb_pyre.auth()
    email = user_dict['email']
    res = hashlib.sha256(email.encode())
    sha_email = res.hexdigest()
    result = fb.post('/{}'.format(sha_email), user_dict)
    flag = auth.create_user_with_email_and_password(email, user_dict['password'])
    if result != None and flag != None:
        status = True
        return status


##------------------------------------------------------------------------------##
##__________________pages__________________________
@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login_page')
def login_page():
    return render_template('login.html')



@app.route('/signup_page')
def accounts_page():
    return render_template('signup.html')


@app.route('/account_details_page')
def account_details_page():
    if 'username' in session:
        return render_template('account_details.html')
    else:
        print('Please Login')
        return render_template('login.html')


@app.route('/index_page')
def index_page():
    if 'username' in session:
        return render_template('index.html')
    else:
        print('Please Login')
        return render_template('login.html')



##________________functional API________________________

@app.route("/review_MN")
def review_MN():
    data = get_data('MN')
    return render_template('review_page.html', hotels_info = data)

@app.route("/review_NC")
def review_NC():
    data = get_data('NC')
    return render_template('review_page.html', hotels_info = data)

@app.route("/review_WI")
def review_WI():
    data = get_data('WI')
    return render_template('review_page.html', hotels_info = data)

@app.route("/review_CT")
def review_CT():
    data = get_data('CT')
    return render_template('review_page.html', hotels_info = data)

@app.route("/review_VA")
def review_VA():
    data = get_data('VA')
    return render_template('review_page.html', hotels_info = data)





@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username')
    for fname in os.listdir(os.path.join('static', 'temp')):
        os.remove(os.path.join('static', 'temp', fname))
    print(session)
    return render_template('login.html')




@app.route("/login", methods = ['POST'])
def login():
    email = request.form['email']
    password = request.form['pass']
    valid = logincheck(email, password)
    if valid:
        session['logged_in'] = True
        session['username'] = email
        print(session)
        return render_template('index.html')
    else:
        flash('Incorrect Username or Password')
        print('Incorrect Username or Password')
        return render_template('login.html')



@app.route("/signup", methods = ['POST'])
def signup():
    user = {}
    user['name'] = request.form['name']
    user['email'] = request.form['email']
    user['password'] = request.form['pass']
    valid, msg = signupcheck(user)
    print(valid, msg)
    if valid:
        status = update_db(user)
        if status:
            flash(msg)
            print(msg)
            return render_template('login.html')
        else:
            flash('Error in creating profile')
            print('Error in creating profile')
            return render_template('signup.html')
    else:
        flash(msg)
        print(msg)
        return render_template('signup.html')




if __name__ == "__main__":
    app.secret_key = os.urandom(100)
    app.run(host='0.0.0.0', port=5000, debug = True )
