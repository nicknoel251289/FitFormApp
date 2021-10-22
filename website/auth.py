# 1. This is a blueprint of our application; it has a bunch of routes/URLs defined inside of it.
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User

from flask_login import login_user, login_required, logout_user, current_user

# 1. so we never store a password in plain text
# 2. hash functions are one way and do not have a reverse. You pass the password as an argument
#    and the hash function spits out a hash. With that hash, you can never figure out the original
#    password. You can reverse the function. The only way to check that the password is the same
#    is to pass the same password as an argument and compare the hashes
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

# 1. Should name the blueprint var the same name as the file for ease of use
auth = Blueprint('auth', __name__)

# 1. Define a view(route)
# 2. The argument is the URL/endpoint we want to use and below is the function we bind to it.
# 3. The return value of the function is what is shown in the browser when we hit the 
#    endpoint/route we passed.
# 4. We register the blueprints in the __init_.py. This tells the app we have blueprints that
#    contain different views/URLs/endpoint for our app and where they are
# 5. We only have the 1 blueprint, auth, so this will include all the below routes 

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # 1. if we are submitting a login (post)
    if request.method == 'POST':
        # 2. get the email/password from the DB based on what they provided in the email/password field of the login
        email = request.form.get('email').lower()
        password = request.form.get('password')
        # 3. validate if the user has an account by querying the DB and filtering through columns for the email that
        #    is passed to the filter_by function
        # 4. each user must have a unique email so filtering by the first should give us the one and only if an account exists
        user = User.query.filter_by(email=email).first()
        if user:
            # 1. compare if user.password (password from DB) and password (from the login form) are the same
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # 2. login the current user
                # 3. the remember=True keeps track of whether the user is logged in until they clear their 
                #    session/browsing history or log out
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Could not find account assocciated with the email provided.', category='error')

    return render_template("login.html", user=current_user)

# 1. The login required means that we cannot access this page/route unless they are logged in.
# 2. We don't want someone to be able to logout if they are not logged in
@auth.route('/logout')
@login_required
def logout():
    # 1. You do not need to pass the user to log them out
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign up', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        first_name = request.form.get('first_name')
        password_1 = request.form.get('password_1')
        password_2 = request.form.get('password_2')

        # 1. check if account already exists when signing up
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account with the provided email already exists.', category='message')
            return redirect(url_for('auth.login'))
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be longer than 2 characters.', category='error')
        elif password_1 != password_2:
            flash('Passwords don\'t match.', category='error')
        elif len(password_1) < 7:
            flash('Password must be longer than 7 characters.', category='error')
        else:
            # 1. define the user, using the table scheme we defined/blueprinted out in our models.py
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password_1, method='sha256'))
            # 1. add user to DB
            db.session.add(new_user)
            db.session.commit()

            # 1. login the new_user
            login_user(new_user, remember=True)

            flash('Account created successfully.', category='success')

            # 1. redirect to home page after successful login
            # 2. url_for finds the URL assocciated with the home function
            # 3. views is our blueprint (views.py) and home is our function we will invoke
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

# 1. Passing arguments is the second+ argument we pass. It can be a variable, a string, or any data type
# 2. Then in the login.html template, we can use {{ text }} and our message will be passed
# 3. Routes need to know when we send a type of request (GET, POST, UPDATE, DELETE, etc); based on the type of request,
#    the page will do something differently.
#    We can define the types of methods that the route can accept
# 4. When we land on the route, it's a GET request and when we submit the form, it is a POST request
# 5. If we want to get the data we sent in the form, we can use "data = request.form". The request variable; whenever accessed
#    inside of a route, it will have info about the request that was sent, to access the route it is used in. The form property,
#    has all of the data that was sent as part of form.
# 6. Flask has an import object, flash, that allows you to flash messages on the screen.
@auth.route('/testing page', methods=['POST'])
def testingPage():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password_1 = request.form.get('password_1')
        password_2 = request.form.get('password_2')

        if len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be longer than 2 characters', category='error')
        elif password_1 != password_2:
            flash('Passwords don\'t match.', category='error')
        elif len(password_1) < 7:
            flash('Password must be longer than 7 characters', category='error')
        else:
            flash('Account created successfully.', category='success')
            print(request.form)

    return render_template("testing_page.html", text="this is a text message", username="some name", boolean=True, isNick=False)