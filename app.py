from flask import Flask, render_template, request, send_file, flash, redirect, session, abort
import re
import pyrebase

app = Flask(__name__)

root_dir = '.'

config = {
  "apiKey": "AIzaSyDhyp_l-BjhR3WJq6AsOu64cFf96sOg4qw",
  "authDomain": "bsic-ff4c8.firebaseapp.com",
  "databaseURL": "https://bsic-ff4c8.firebaseio.com",
  "storageBucket": "bsic-ff4c8.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def index():
	if session.get('logged_in') or session.get('dealer_logged_in'):
		return render_template('index.html', user=session['user'])
	else:
		return render_template('index.html')

@app.route('/demo', methods=['GET', 'POST'])
def demo():
	if request.method == 'POST' and 'cname' in request.form and 'camount' in request.form and 'copen' in request.form and 'cclose' in request.form and 'cduration' in request.form and 'clocation' in request.form:
		with open(root_dir + "/demo/contracts.txt", "a") as demo:
			demo.write(request.form['cname'] + " " + request.form['camount'] + " " + request.form['copen'] + " " + request.form['cclose'] + " " + request.form['cduration'] + " " + request.form['clocation'] + "\n")
			newfile = open(root_dir + "/tenders/" + request.form['cname'] + ".txt", "w+")
			newfile.close()

	all_contracts = []
	with open(root_dir + "/demo/contracts.txt", "r") as reader:
		for line in reader:
			all_contracts.append(line.split()[:6])

	if session.get('logged_in') or session.get('dealer_logged_in'):
		return render_template('demo.html', all_contracts=all_contracts, user=session['user'])
	else:
		return render_template('demo.html', all_contracts=all_contracts)

@app.route('/tender/<tender_title>', methods=['GET', 'POST'])
def this_tender(tender_title):
	session['tender_title'] = tender_title
	with open(root_dir + "/demo/contracts.txt", "r") as reader:
		for line in reader:
			if(line.split()[0] == tender_title):
				wanted = line
				break

	if session.get('user'):
		f = open(root_dir + "/tenders/" + tender_title + ".txt", "r")
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
		return render_template('tender.html', user=session['user'], all_my_bids=bids.split(), data=wanted.split())

	if request.method == 'POST' and 'bidamount' in request.form:

		with open(root_dir + "/tenders/" + tender_title + ".txt", "a") as bidder:
			bidder.write(session['user'] + "-" + request.form['bidamount'] + "\n")

		session['bid_submitted'] = True
		return render_template('portal.html', user=session['user'])

	if session.get('logged_in') or session.get('dealer_logged_in'):

		if session['bid_submitted'] == True:
			return render_template('tender.html', user=session['user'], status="BID SUBMITTED", amount=calcbid, data=wanted.split())
		else:
			return render_template('tender.html', user=session['user'], data=wanted.split())
	else:
		return render_template('login.html')

@app.route('/userpage', methods=['GET', 'POST'])
def userpage():
	if session.get('logged_in'):
		return render_template('userpage.html', username=session['user'])
	else:
		return render_template('index.html')

@app.route('/addTender', methods=['GET', 'POST'])
def addTender():
	if request.method == 'POST':
		with open(root_dir + "/demo/contracts.txt", "a") as demo:
			demo.write(request.form['org'] + " " + request.form['tenderref'] + " " + request.form['tenderid'] + " " + request.form['tenderstatus'] + " " + request.form['tendercat'] + " " + request.form['techdetails'] + " " + request.form['financedetails'] + " " + request.form['bidopen'] + " " + request.form['bidclose'] + " " + request.form['tenderval'] + "\n")
			newfile = open(root_dir + "/tenders/" + request.form['tenderref'] + ".txt", "w+")
			newfile.close()

	if session.get('dealer_logged_in'):
		return render_template('addTender.html', username=session['user'])
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
		accs = db.child("accounts").child('supplier').get()
		for idx in accs.each():
			if(idx.val()[request.form['dealerusername']]):
				session['logged_in'] = True
				session['user'] = request.form['dealerusername']
				return render_template('index.html', user=session['user'])

	if request.method == 'POST' and 'contractorusername' in request.form and 'contractorpassword' in request.form:
		accs = db.child("accounts").child('clients').get()
		for idx in accs.each():
			if(idx.val()[request.form['contractorusername']]):
				session['logged_in'] = True
				session['user'] = request.form['contractorusername']
				return render_template('index.html', user=session['user'])

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
		db.child("accounts").child("clients")
		data = {request.form['contractorusername'] : request.form['contractorpassword']}
		db.push(data)
		return render_template('registerdetails.html')
	else:
		flash('wrong password!')

	if request.method == 'POST' and 'dealerusername' in request.form and 'dealerpassword' in request.form:
		db.child("accounts").child("supplier")
		dat = {request.form['dealerusername'] : request.form['dealerpassword']}
		db.push(dat)
		return render_template('registerdetails.html')
	else:
		flash('wrong password!')

	return render_template('register.html')

@app.route('/tender', methods=['GET', 'POST'])
def tender():

	if request.method == 'POST' and 'bidamount' in request.form:
		print(session['tender_title'] + "hello")

		with open(root_dir + "/tenders/" + session['tender_title'] + ".txt", "a") as bidder:
			bidder.write(session['user'] + "-" + request.form['bidamount'] + "\n")

		session['bid_submitted'] = True
		return render_template('index.html', user=session['user'])

@app.route('/developers', methods=['GET', 'POST'])
def developers():
	if session.get('logged_in') or session.get('dealer_logged_in'):
		return render_template('developers.html', user=session['user'])
	else:
		return render_template('developers.html')

app.secret_key = "helloworld this is satoshi"

if __name__ == '__main__':
	app.run(debug=True)