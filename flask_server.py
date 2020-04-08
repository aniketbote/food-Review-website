from flask import Flask, render_template, request, session, jsonify, flash
from firebase import firebase
import pyrebase
import hashlib
import os
import time
import cv2
import numpy as np
import pandas as pd

review_data = pd.read_csv('new1.csv')


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
    data_subset = review_data[review_data['Category'] == pro]
    for name in list(set(data_subset['Restaurant Name'])):
        hdict = {}
        hotel_subset = data_subset[data_subset['Restaurant Name'] == name]
        hdict['Restaurant Name'] = name
        hdict['Address'] = list(hotel_subset['Address'])[0]
        hdict['Rating text'] = list(hotel_subset['Rating text'])[0]
        hdict['image_name'] = os.path.join('res_images', name + '.png')
        # print(hdict['image_name'])
        hotels.append(hdict)
    return hotels


def get_data_single(res):
    hdict = {}
    hotel_subset = review_data[review_data['Restaurant Name'] == res]
    hdict['Restaurant Name'] = res
    hdict['Reviews'] = list(hotel_subset['Reviews'])
    hdict['User_email'] = list(hotel_subset['User_email'])
    hdict['Has Table booking'] = list(hotel_subset['Has Table booking'])[0]
    hdict['Average Cost for two'] = list(hotel_subset['Average Cost for two'])[0]
    hdict['Category'] = list(hotel_subset['Category'])[0]
    hdict['Address'] = list(hotel_subset['Address'])[0]
    hdict['Cuisines'] = list(hotel_subset['Cuisines'])[0]
    hdict['Has Online delivery'] = list(hotel_subset['Has Online delivery'])[0]
    hdict['Aggregate rating'] = list(hotel_subset['Aggregate rating'])[0]
    hdict['Rating text'] = list(hotel_subset['Rating text'])[0]
    hdict['Votes'] = list(hotel_subset['Votes'])[0]
    # hdict['image'] = cv2.imread(os.path.join('static','res_images', name + '.png'))
    hdict['image_name'] = os.path.join('res_images', res + '.png')
    return hdict



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
    if 'username' in session:
        return render_template('index_loggedin.html', username = session['username'])
    else:
        return render_template('index.html')

@app.route('/index_page')
def index_page():
    if 'username' in session:
        return render_template('index_loggedin.html', username = session['username'])
    else:
        return render_template('index.html')



@app.route('/login_page')
def login_page():
    if 'username' in session:
        return render_template('index_loggedin.html', username = session['username'])
    else:
        return render_template('login.html')

@app.route('/about')
def about_page():
    if 'username' in session:
        return render_template('about_loggedin.html', username = session['username'])
    else:
        return render_template('about.html')

@app.route('/contact')
def contact_page():
    if 'username' in session:
        return render_template('contact_loggedin.html', username = session['username'])
    else:
        return render_template('contact.html')



@app.route('/signup_page')
def accounts_page():
    if 'username' in session:
        return render_template('index_loggedin.html', username = session['username'])
    else:
        return render_template('signup.html')






##________________functional API________________________

@app.route("/bestofmumbai")
def review_MN():
    if 'username' in session:
        data = get_data(1)
        return render_template('bestofmumbai.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/alldaycafe")
def review_NC():
    if 'username' in session:
        data = get_data(2)
        return render_template('alldaycafe.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/kebabs")
def review_WI():
    if 'username' in session:
        data = get_data(3)
        return render_template('kebabs.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/oldisgold")
def review_CT():
    if 'username' in session:
        data = get_data(4)
        return render_template('oldisgold.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/corporate")
def review_VA():
    if 'username' in session:
        data = get_data(5)
        return render_template('corporate.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/streetsavy")
def review_NY():
    if 'username' in session:
        data = get_data(6)
        return render_template('streetsavy.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')


@app.route("/show_info",methods=["POST"])
def show_info():
    if 'username' in session:
        res = request.form['res_name']
        print(res)
        data = get_data_single(res)
        return render_template('show_info.html', data = data)
    else:
        return render_template('login.html')




@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username')
    for fname in os.listdir(os.path.join('static', 'temp')):
        os.remove(os.path.join('static', 'temp', fname))
    print(session)
    return render_template('index.html')




@app.route("/login", methods = ['POST'])
def login():
    email = request.form['email']
    password = request.form['pass']
    valid = logincheck(email, password)
    if valid:
        session['logged_in'] = True
        session['username'] = email
        print(session)
        return render_template('index_loggedin.html', username = session['username'])
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
