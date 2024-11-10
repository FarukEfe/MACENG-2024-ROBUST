# API & SQL
from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
# Formatting
import re, base64, io
from PIL import Image
# To encrypt/decrypt passwords
from cryptography.fernet import Fernet
#import encryption


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e6d7g8h9i10'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = "robusts3169" #Replace ******* with  your database password.
app.config['MYSQL_DB'] = 'loginapp'


# Intialize MySQL
mysql = MySQL(app)


# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        #log_img = request.form['image']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Encryption
        cursor.execute('SELECT id FROM accounts WHERE username LIKE %s', [username])
        id = cursor.fetchone()
        cursor.execute('SELECT key FROM keys WHERE id = %s', [id])
        key = cursor.fetchone()
        cipher = Fernet(key)
        encrypted_password = cipher.encrypt(password.encode())
        # Fetch image for username and compare with 
        cursor.execute('SELECT image FROM accounts WHERE username LIKE %s', [username])
        image = cursor.fetchone()
        '''
        if image:
            
            image = image[0]
            # Load the image from binary data using PIL
            image = Image.open(io.BytesIO(image))   
        else:
            return {{ "access": "denied", "message": "User face image doesn't match"}}
        '''
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, encrypted_password))
        # cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
                # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username/password!", "danger")
    return render_template('auth/login.html',title="Login")


# http://localhost:5000/pythonlogin/register 
# This will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        image = request.form['image']
        #image = image.split(',')[1]
        #image = base64.b64decode(image)
                # Check if account exists using MySQL
        # Generate key & Encrypt Password
        key = Fernet.generate_key()
        cipher = Fernet(key)
        encrypted_password = cipher.encrypt(password.encode())
        # Get cursor to sql connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        cursor.execute( "SELECT * FROM accounts WHERE username LIKE %s", [username])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash("Account already exists!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash("Username must contain only characters and numbers!", "danger")
        elif not username or not password or not email:
            flash("Incorrect username/password!", "danger")
        else:
            # Before:
            '''
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (username,email, password, image))
            mysql.connection.commit()
            flash("You have successfully registered!", "success")
            return redirect(url_for('login')
            '''
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (username, email, encrypted_password, image))
            mysql.connection.commit()
            cursor.execute('SELECT id FROM accounts where WHERE username LIKE %s', [username])
            id = cursor.fetchone()
            cursor.execute('INSERT INTO keys VALUES (%d, %s)', (id, key))
            mysql.connection.commit()
            flash("You have successfully registered!", "success")
            return redirect(url_for('login'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Please fill out the form!", "danger")
    # Show registration form with message (if any)
    return render_template('auth/register.html',title="Register")

# http://localhost:5000/pythinlogin/home 
# This will be the home page, only accessible for loggedin users

@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home/home.html', username=session['username'],title="Home")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))    


@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('auth/profile.html', username=session['username'],title="Profile")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))  

if __name__ =='__main__':
	app.run(debug=True)
