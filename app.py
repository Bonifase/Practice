from flask import Flask, render_template, request, redirect, url_for, session, flash, logging
from wtforms import Form, StringField, PasswordField, validators, TextField, BooleanField,DateField
import os
from passlib.hash import sha256_crypt
from flask_login import LoginManager
from functools import wraps



app = Flask(__name__)
app.config.from_object(__name__) # load config from this file , app.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'app.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('APP_SETTINGS', silent=True)
user = []
shopping_list = []
store = {}



class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min = 1, max = 20)])
    username = StringField('Username', [validators.Length(min = 1, max = 30)])
    email = StringField('Email', [validators.Length(min = 2, max = 20)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message = 'Password do not match')])
    confirm = PasswordField('Confirm password')

class LogninForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min = 1, max = 30)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min = 5, max = 80)])
    remember = BooleanField('Remember Me')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/lists')
def lists():
     Lists = shopping_list
     for item in Lists:
        return render_template("lists.html", Lists=Lists)
     else:
        msg = 'No List Found'
        return render_template("lists.html", msg=msg)
    

@app.route('/alist/<string:Title>/')
def alist(Title):
    return render_template('alist.html', Title = Title)


@app.route('/register', methods = ['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        #Get form data
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        #Insert the form data in the user list
        if email not in user and username not in user:
            user.append(name)
            user.append(email)
            user.append(username)
            user.append(password)
            session['logged_in'] = True
            session['Username'] = username
            flash('Registration successful.', 'success')
            return redirect(url_for('home'))
        else:
            flash('User already Registered.', 'danger')
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)

#User login
@app.route('/login', methods = ['POST', 'GET'])
def login():
    
    form = LogninForm(request.form)
    if request.method == 'POST':
         #Get data from the form
         username = request.form['username']
         password_cadidate = request.form['password']
         #Check if username and password exist in the user dictionary  
         if username in user and  password_cadidate in user:
            session['logged_in'] = True
            session['Username'] = username
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))
         else:
            error = 'Wrong Login Details'
            return render_template('login.html', error=error)
         
    else:
        return render_template('login.html')

#check  if user is logged in
def is_logged_in(f):
     @wraps(f)
     def wrap(*args, **kwargs):
         if 'logged_in' in session:
             return f(*args, **kwargs)
         else:
             flash('Unauthorised, please login', 'danger')
             return redirect(url_for('login'))
     return wrap

#Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are loogged out!', 'success')
    return redirect(url_for('home'))


#Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    Lists = shopping_list 
    for item in Lists:
        return render_template("dashboard.html", Lists=Lists)
    else:
        msg = 'No List Found'
        return render_template("dashboard.html", msg=msg)
    

#List Form class
class addForm(Form):
    Id = StringField('Id', [validators.Length(min = 1, max = 1000)])
    Title = StringField('Title', [validators.Length(min = 3, max = 10)])
    Quantity = StringField('Quantity', [validators.Length(min = 1, max = 100000)])
    Date = DateField('Date', format='%Y-%m-%d')
    
#Add list
@app.route('/add_list', methods=['GET', 'POST'])
@is_logged_in
def add_list():
    form = addForm(request.form)
    if request.method == 'POST' and form.validate():
        Id = form.Id.data
        title = form.Title.data
        qnty = form.Quantity.data
        date = form.Date.data
        store['Id'] = Id
        store['Title'] = title
        store['Quantity'] = qnty
        store['Date'] = date
        shopping_list.append(store)

        flash('List created', 'success')
        return redirect(url_for('dashboard'))

    return render_template("add_list.html", form=form)


#Edit list
@app.route('/edit_list/<string:Id>', methods=['GET', 'POST'])
@is_logged_in
def edit_list(Id):
    form = addForm(request.form)
    #get item by title
    for item in store:
        #populate form fields
        form.Id.data = store['Id']
        form.Title.data = store['Title']
        form.Quantity.data = store['Quantity']
        form.Date.data = store['Date']
        if request.method == 'POST' and form.validate():
            Id = request.form['Id']
            title = request.form['Title']
            qnty = request.form['Quantity']
            date = request.form['Date']
            store['Id'] = Id
            store['Title'] = title
            store['Quantity'] = qnty
            store['Date'] = date
            shopping_list.append(store)

            flash('List edited', 'success')
            return redirect(url_for('dashboard'))

        return render_template("edit_list.html", form=form)
    else:
        msg = 'No List Found'
        return render_template("dashboard.html", msg=msg)
        
#Delete list        
@app.route('/delete_list/<string:Id>', methods=['POST'])
@is_logged_in
def delete_list(Id):
    for item in store:
       
    
        del store['Id']
        del store['Title']
        del store['Quantity']
        del store['Date']
        

        flash('Item Removed', 'success')
        return redirect(url_for('dashboard'))
    else:
        msg = 'No List Found'
        return render_template("dashboard.html", msg=msg)


if __name__ == "__main__":
    app.secret_key='ThisIsSecret'
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
