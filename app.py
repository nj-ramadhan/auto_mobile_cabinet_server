# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import uuid


app = Flask(__name__)


app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'auto_mobile_cabinet_server'


mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		organisation = request.form['organisation']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']
		postalcode = request.form['postalcode']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'name must contain only characters and numbers !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (username, password, email, organisation, address, city, state, country, postalcode, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)


@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("index.html")
	return redirect(url_for('login'))


@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'], ))
		account = cursor.fetchone()
		return render_template("display.html", account = account)
	return redirect(url_for('login'))

@app.route("/update", methods =['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			organisation = request.form['organisation']
			address = request.form['address']
			city = request.form['city']
			state = request.form['state']
			country = request.form['country']
			postalcode = request.form['postalcode']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
			account = cursor.fetchone()
			if account:
				msg = 'Account already exists !'
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'Invalid email address !'
			elif not re.match(r'[A-Za-z0-9]+', username):
				msg = 'name must contain only characters and numbers !'
			else:
				cursor.execute('UPDATE accounts SET username =% s, password =% s, email =% s, organisation =% s, address =% s, city =% s, state =% s, country =% s, postalcode =% s WHERE id =% s', (username, password, email, organisation, address, city, state, country, postalcode, (session['id'], ), ))
				mysql.connection.commit()
				msg = 'You have successfully updated !'
		elif request.method == 'POST':
			msg = 'Please fill out the form !'
		return render_template("update.html", msg = msg)
	return redirect(url_for('login'))

@app.route("/search", methods =['GET', 'POST'])
def search():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'nama_dokumen' in request.form:
			try:
				nama_dokumen = request.form['nama_dokumen']
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('SELECT id_dokumen FROM list_dokumen WHERE nama_dokumen = % s', (nama_dokumen, ))
				id_dokumen = cursor.fetchone()['id_dokumen']
				print(id_dokumen)
				mysql.connection.commit()

				id = uuid.uuid1()
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('INSERT INTO data_trans SET id_dokumen =% s, id_transaksi =% s', (id_dokumen, id.hex))
				mysql.connection.commit()
				msg = 'Wait While we prepare your Document !'
			except:
				msg = 'Document you find is note Stored !'
			
		return render_template("search.html", msg = msg)
	return redirect(url_for('login'))

@app.route("/store", methods =['GET', 'POST'])
def store():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'nama_dokumen' in request.form and 'device_ke' in request.form and 'rak_ke' in request.form and 'baris_ke' in request.form and 'kolom_ke' in request.form:
			try:
				nama_dokumen = request.form['nama_dokumen']
				device_ke = request.form['device_ke']
				rak_ke = request.form['rak_ke']
				baris_ke = request.form['baris_ke']
				kolom_ke = request.form['kolom_ke']
				
				
				id = uuid.uuid1()
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('SELECT * FROM list_dokumen WHERE nama_dokumen = % s', (nama_dokumen, ))
				account = cursor.fetchone()
				if account:
					msg = 'Nama Dokumen sudah ada !'
				elif not re.match(r'[A-Za-z0-9]+', nama_dokumen):
					msg = 'Nama dokumen hanya boleh terdiri dari huruf and angka !'
				else:
					cursor.execute('INSERT INTO list_dokumen VALUES (% s, % s, % s, % s, % s, % s)', (id.hex, nama_dokumen, device_ke, rak_ke, baris_ke, kolom_ke, ))
					mysql.connection.commit()
					msg = 'Document data is sucesfully registered !'
			except:
				msg = 'Document registration error !'

		elif request.method == 'POST':
			msg = 'Please fill out the form  !'
			
		return render_template("store.html", msg = msg)


if __name__ == "__main__":
	# app.run(host ="localhost", port = int("5000"))
	app.run(host ="0.0.0.0", port = int("5000"))
