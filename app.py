from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = firebaseConfig = {
	"apiKey": "AIzaSyCBRoPeva9PjMfgkdbNk8dP6r9H8b0YRB0",
	"authDomain": "washington-dc-b7cb5.firebaseapp.com",
	"projectId": "washington-dc-b7cb5",
	"storageBucket": "washington-dc-b7cb5.appspot.com",
	"messagingSenderId": "461911160217",
	"appId": "1:461911160217:web:b7985d0f7b5994bc340f08",
	"measurementId": "G-702E43P61D",
 	"databaseURL": "https://washington-dc-b7cb5-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def home_page():
	return render_template("home.html")

@app.route('/add-comment', methods=['GET', 'POST'])
def add_comment():
	return redirect(url_for('signin'))

@app.route('/sigin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home_page'))
        except:
            return redirect(url_for('signup'))

    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"full_name":request.form['full_name'], "password":request.form['password'], "username": request.form['username'], "bio":request.form['bio']}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return render_template("comments.html")
        except:
        	error = "Authentication failed"

    return render_template("signup.html")

if __name__ == '__main__':
    app.run(debug=True)