from flask import Flask, render_template, request, send_file, flash, redirect, session, abort
import re
import pyrebase

app = Flask(__name__)

root_dir = '/home/teamsatoshi/936a185caaa266bb9cbe981e9e05cb.github.io'

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
	accs = db.child("tenders").child('all_tenders').get()
	reqel = 1
	for idx in accs.each():
		try:
			if(idx.val()['org'] == tender_title):
				reqel = idx.val()
				myqel = idx.key()
		except KeyError:
			print("foo")

	accs2 = db.child("bidders").child('confirmed').get()
	checker = -1
	for idx in accs2.each():
		try:
			if(idx.val()[session['user']] == "confirmed" or idx.val()[session['user']] == "failed"):
				xeqel = idx.val()
				xmyqel = idx.key()
				checker = 1
				break
		except KeyError:
			print("foo")

	tender_details = []
	print(reqel)
	tender_details.extend([reqel['bidclose'], reqel['bidop'], reqel['bidopen'], reqel['clare'], reqel['clars'], reqel['downde'], reqel['downds'], reqel['financedetails'], reqel['formcont'], reqel['gentech'], reqel['iem'], reqel['meetadd'], reqel['meetdate'], reqel['mulca'], reqel['org'], reqel['paymode'], reqel['payto'], reqel['pera'], reqel['pername'], reqel['preq'], reqel['pubd'], reqel['techdetails'], reqel['tendercat'], reqel['tenderid'], reqel['tenderref'], reqel['tenderstatus'], reqel['tenderval'], reqel['tfe'], reqel['titlec'], reqel['workd']])

	try:
		if(reqel[session['user']] != "vzxjhjxhcjxhuhxxx"):
			print("yay")
	except KeyError:
		db.child("tenders").child("all_tenders").child(myqel).update({session['user']: "false"})
		allownow = True

	if(session.get('logged_in') and checker == -1):
		db.child("bidders").child("confirmed")
		db.push({session['user']: "failed"})
		return render_template('registerdetails.html', user=session['user'])

	if(session.get('logged_in') and xeqel[session['user']] != "confirmed"):
		return render_template('registerdetails.html', user=session['user'])

	if request.method == 'POST' and 'bidamt' in request.form:
		db.child("tenders").child("all_tenders").child(myqel).update({session['user']: "true"})
		return render_template('tender.html', user=session['user'], data=tender_details, isOpen="true", hasBid="true")

	if request.method == 'POST':
		db.child("tenders").child("all_tenders").child(myqel).update({"tenderstatus": "false"})
		return render_template('tender.html', user=session['user'], data=tender_details, isOpen="false")

	if session.get('logged_in') and (reqel['tenderstatus'] == "true") and (reqel[session['user']] == "true"):
		return render_template('tender.html', user=session['user'], data=tender_details, isOpen="true", hasBid="true")

	if session.get('logged_in') and (reqel['tenderstatus'] == "true") and (reqel[session['user']] == "false"):
		return render_template('tender.html', user=session['user'], data=tender_details, isOpen="true", hasBid="false")

	if session.get('logged_in') and (reqel['tenderstatus'] == "true") and allownow == True:
		return render_template('tender.html', user=session['user'], data=tender_details, isOpen="true", hasBid="false")

	if session.get('dealer_logged_in') and (reqel['tenderstatus'] == "true"):
		return render_template('tender.html', user=session['user'], data=tender_details, isOpen="true")

	if session.get('logged_in') and (reqel['tenderstatus'] != "true"):
		return render_template('tender.html', user=session['user'], data=tender_details, isOpen="false")

	if session.get('dealer_logged_in') and (reqel['tenderstatus'] != "true"):
		return render_template('tender.html', user=session['user'], data=tender_details, isOpen="false")

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
		db.child("tenders").child("all_tenders")
		data = {"org" : request.form['org'], "tenderref" : request.form['tenderref'], "tenderid" : request.form['tenderid'], "tenderstatus" : request.form['tenderstatus'], "tendercat" : request.form['tendercat'], "techdetails" : request.form['techdetails'], "financedetails" : request.form['financedetails'], "bidopen" : request.form['bidopen'], "bidclose" : request.form['bidclose'], "tenderval" : request.form['tenderval'], "paymode" : request.form['paymode'], "payto" : request.form['payto'], "gentech" : request.form['gentech'], "formcont" : request.form['formcont'], "titlec" : request.form['titlec'], "workd" : request.form['workd'], "preq" : request.form['preq'], "meetadd" : request.form['meetadd'], "meetdate" : request.form['meetdate'], "bidop" : request.form['bidop'], "pubd" : request.form['pubd'], "downds" : request.form['downds'], "downde" : request.form['downde'], "clars" : request.form['clars'], "clare" : request.form['clare'], "iem" : request.form['iem'], "tfe" : request.form['tfe'], "pername" : request.form['pername'], "pera" : request.form['pera'], "mulca" : request.form['mulca']}
		db.push(data)
		return render_template('index.html')

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
			try:
				if(idx.val()[request.form['dealerusername']] == request.form['dealerpassword']):
					session['dealer_logged_in'] = True
					session['user'] = request.form['dealerusername']
					return render_template('index.html', user=session['user'])
			except KeyError:
				print("foo")

	if request.method == 'POST' and 'contractorusername' in request.form and 'contractorpassword' in request.form:
		accs = db.child("accounts").child('clients').get()
		for idx in accs.each():
			try:
				if(idx.val()[request.form['contractorusername']] == request.form['contractorpassword']):
					session['logged_in'] = True
					session['user'] = request.form['contractorusername']
					return render_template('index.html', user=session['user'])
			except KeyError:
				print("foo")

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
		session['user'] = request.form['contractorusername']

		db.child("bidders").child("confirmed")
		dat = {session['user'] : "failed"}
		db.push(dat)

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

@app.route('/registerdetails', methods=['GET', 'POST'])
def registerdetails():

	accs = db.child("bidders").child('confirmed').get()
	for idx in accs.each():
		try:
			if(idx.val()[session['user']] == "failed"):
				thisone = idx.key()
		except KeyError:
			print("foo")

	if request.method == 'POST':
		db.child("bidders").child("confirmed").child(thisone).update({session['user']: "confirmed"})
		session['logged_in'] = True
		print(thisone)
		return render_template('index.html', user=session['user'])

	return render_template('registerdetails.html')

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