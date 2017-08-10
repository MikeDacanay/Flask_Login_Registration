from flask import Flask, request, render_template, redirect, flash
# from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
app.secret_key= "Jade"

@app.route('/')
def index():		
	return render_template('index.html')

@app.route('/log', methods=["POST"])
def log():
	print request.form['email_log']
	print request.form['pass_log']		
	return redirect('/')
	
app.run(debug=True)
