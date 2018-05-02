from flask import Flask, render_template, request, send_file, flash, redirect, session, abort
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if session.get('logged_in') or session.get('dealer_logged_in'):
		return render_template('index.html', user=session['user'])
	else:
		return render_template('index.html')

@app.route('/portal', methods=['GET', 'POST'])
def portal():
	if session.get('logged_in') or session.get('dealer_logged_in'):
		return render_template('portal.html', user=session['user'])
	else:
		return render_template('portal.html')

@app.route('/whitepaper', methods=['GET', 'POST'])
def whitepaper():
	if session.get('logged_in') or session.get('dealer_logged_in'):
		return render_template('whitepaper.html', user=session['user'])
	else:
		return render_template('whitepaper.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST' and 'dealerusername' in request.form and 'dealerpassword' in request.form:
		f = open("./users/dealers/dealers.txt", "r")
		creds = f.read()
		f.close()

		start = (re.search(request.form['dealerusername'], creds).start() + len(request.form['dealerusername'])) + 1 
		calcpwd = creds[start:start + len(request.form['dealerpassword'])]
		if request.form['dealerusername'] in creds and request.form['dealerpassword'] == calcpwd :
			session['dealer_logged_in'] = True
			session['user'] = request.form['dealerusername']
			render_template('index.html', user=session['user'])
		else:
			flash('wrong password!')

	if request.method == 'POST' and 'contractorusername' in request.form and 'contractorpassword' in request.form:
		f = open("./users/contractors/contractors.txt", "r")
		creds = f.read()
		f.close()

		start = (re.search(request.form['contractorusername'], creds).start() + len(request.form['contractorusername'])) + 1 
		calcpwd = creds[start:start + len(request.form['contractorpassword'])]
		if request.form['contractorusername'] in creds and request.form['contractorpassword'] == calcpwd :
			session['logged_in'] = True
			session['user'] = request.form['contractorusername']
			render_template('index.html', user=session['user'])
		else:
			flash('wrong password!')

	return render_template('login.html')

@app.route("/logout")
def logout():
	session['logged_in'] = False
	session['dealer_logged_in'] = False
	return index()

@app.route('/register', methods=['GET', 'POST'])
def register():
	if session.get('logged_in') or session.get('dealer_logged_in'):
		return render_template('register.html', user=session['user'])

	if request.method == 'POST' and 'contractorusername' in request.form and 'contractorpassword' in request.form:
			with open("./users/contractors/contractors.txt", "a") as bidder:
				bidder.write(request.form['contractorusername'] + "-" + request.form['contractorpassword'] + "\n")

			render_template('index.html')
	else:
		flash('wrong password!')

	if request.method == 'POST' and 'dealerusername' in request.form and 'dealerpassword' in request.form:
			with open("./users/dealers/dealers.txt", "a") as bidder:
				bidder.write(request.form['dealerusername'] + "-" + request.form['dealerpassword'] + "\n")

			render_template('index.html')
	else:
		flash('wrong password!')	

	return render_template('register.html')

@app.route('/tender', methods=['GET', 'POST'])
def tender():

	f = open("./tenders/t1/bids.txt", "r")
	bids = f.read()
	bidsearch = re.search(session['user'], bids)
	if bidsearch is not None:
		start = bidsearch.start() + len(session['user']) + 1 
		calcbid = bids[start:start + 5]
		session['bid_submitted'] = True
	else:
		calcbid = str(0)
		session['bid_submitted'] = False

	if session.get('dealer_logged_in'):
		bids = bids.replace('\n', ' ')
		print(bids)
		return render_template('tender.html', user=session['user'], all_my_bids=bids.split())

	if request.method == 'POST' and 'bidamount' in request.form:

		with open("./tenders/t1/bids.txt", "a") as bidder:
			bidder.write(session['user'] + "-" + request.form['bidamount'] + "\n")

		session['bid_submitted'] = True
		return render_template('portal.html', user=session['user'])

	if session.get('logged_in') or session.get('dealer_logged_in'):

		if session['bid_submitted'] == True:
			return render_template('tender.html', user=session['user'], status="BID SUBMITTED", amount=calcbid)
		else:
			return render_template('tender.html', user=session['user'])
	else:
		return render_template('tender.html')

@app.route('/developers', methods=['GET', 'POST'])
def developers():
	if session.get('logged_in') or session.get('dealer_logged_in'):
		return render_template('tender.html', user=session['user'])
	else:
		return render_template('tender.html')

app.secret_key = "helloworld this is satoshi"

if __name__ == '__main__':
	app.run(debug=True)