from flask import Flask, request, render_template, redirect, flash, session
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
	post_db= mysql.query_db("SELECT messages.id AS Message_ID,message, users_id,CONCAT(first_name,' ',last_name) AS Name,DATE_FORMAT(messages.create_date, '%M %d %Y %T') AS Date FROM messages LEFT JOIN  users ON messages.users_id=users.id ORDER BY Date desc")
	comment_db= mysql.query_db("SELECT messages_id,concat(first_name,' ',last_name) as Name, DATE_FORMAT(comments.create_date, '%M %d %Y %T') AS Date,comment from comments left join users on users_id=users.id")
	print comment_db
	return render_template('wall.html', all_posts=post_db, all_comments=comment_db)

@app.route('/log', methods=["POST"])
def log():
	data_login = mysql.query_db("SELECT email, password,id,first_name,last_name FROM users")

	for login in data_login:
		if login['email']+login['password']==request.form['email_log']+request.form['pass_log']:
			session['id'] = login['id']
			session['name']= login['first_name']+" "+login['last_name']
			# print session['id']
			# print session['name']
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
		flash("vfg!!")
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

@app.route('/poster', methods=['POST'])
def post_content():
	query="INSERT INTO messages(message,create_date,updated_date,users_id) VALUES(:a,NOW(),NOW(),:b)"

	data= {
		'a':request.form['post_content'],
		'b':session['id']
	}

	mysql.query_db(query, data)
	return redirect('/wall')

@app.route('/commentor', methods=['POST'])
def post_comment(): 

	query="INSERT INTO comments(comment,create_date,updated_date,users_id,messages_id) VALUES(:a,NOW(),NOW(),:b,:c)"

	data= {
		'a':request.form['comment_content'],
		'b':session['id'],
		'c':request.form['action'] #IN HTML this input type is hidden
	}

	mysql.query_db(query, data)
	return redirect('/wall')

app.run(debug=True)
