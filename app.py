from flask import Flask, render_template, request, send_file, flash, redirect, session, abort
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if session.get('logged_in'):
		return render_template('index.html', user="ADMIN")
	else:
		return render_template('index.html')

@app.route('/portal', methods=['GET', 'POST'])
def portal():
	if session.get('logged_in'):
		return render_template('portal.html', user="ADMIN")
	else:
		return render_template('portal.html')

@app.route('/whitepaper', methods=['GET', 'POST'])
def whitepaper():
	if session.get('logged_in'):
		return render_template('whitepaper.html', user="ADMIN")
	else:
		return render_template('whitepaper.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		if request.form['password'] == 'password' and request.form['username'] == 'admin':
			session['logged_in'] = True
			render_template('index.html', user="ADMIN")
		else:
			flash('wrong password!')

	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if session.get('logged_in'):
		return render_template('register.html', user="ADMIN")
	else:
		return render_template('register.html')

@app.route('/tender', methods=['GET', 'POST'])
def tender():
	if session.get('bid_submitted'):
		return render_template('tender.html', user="ADMIN", status="BID SUBMITTED")

	if session.get('logged_in'):
		if request.method == 'POST' and 'bidamount' in request.form:
			session['bid_submitted'] = True
			return render_template('tender.html', user="ADMIN", status="BID SUBMITTED")
		else:
			return render_template('tender.html', user="ADMIN")
	else:
		return render_template('tender.html')

@app.route('/developers', methods=['GET', 'POST'])
def developers():
	if session.get('logged_in'):
		return render_template('tender.html', user="ADMIN")
	else:
		return render_template('tender.html')

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(debug=True)