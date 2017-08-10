from flask import Flask, request, render_template, redirect, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app.secret_key= "Jade"

mysql = MySQLConnector(app, 'the_wall')

@app.route('/')
def index():		
	return render_template('index.html')

@app.route('/wall')
def wall():
	return render_template('wall.html')

@app.route('/log', methods=["POST"])
def log():
	data_login = mysql.query_db("SELECT email, password FROM users")

	for login in data_login:
		if login['email']+login['password']==request.form['email_log']+request.form['pass_log']:
			return redirect('/wall')
	flash("Invalid login info"	)

	return redirect('/')

@app.route('/register', methods=['POST'])
def regist():
	data_emails = mysql.query_db("SELECT email FROM users")
	count=0
	if (request.form['first_reg']).isalpha()!=True:
		flash("your FIRST NAME can't CONTAIN NUMBERS, unless... alien?")
		count=1
	if len(request.form['first_reg'])<2:
		flash("your FIRST NAME can't be that SHORT, can it?")
		count=1
	if (request.form['last_reg']).isalpha()!=True:
		flash("your LAST NAME can't CONTAIN NUMBERS, unless... alien?")
		count=1
	if len(request.form['last_reg'])<2:
		flash("your LAST NAME can't be that SHORT, can it?")
		count=1
	if not EMAIL_REGEX.match(request.form['email_reg']):
		flash("hmmm, I can't hack into your email. Must be WRONG EMAIL FORMAT!!")
		count=1
	for x in data_emails:
		if x['email']==request.form['email_reg']:
			flash("Email is already in use!")
			count=1
			break
	if len(request.form['pass_reg'])<9:
		flash("a baby can hack into your account with a SHORT PASSWORD like that")
		count=1
		
	if count>0:
		return redirect('/')


	query="INSERT INTO users(first_name,last_name,email,password,create_date,updated_date) VALUES(:a,:b,:c,:d,NOW(),NOW())"

	data= {
		'a':request.form['first_reg'],
		'b':request.form['last_reg'],
		'c':request.form['email_reg'],
		'd':request.form['pass_reg']
	}

	mysql.query_db(query, data)

	return redirect('/wall')
app.run(debug=True)
