# 1. This is a blueprint of our application; it has a bunch of routes/URLs defined inside of it.
# 2. To render a template, import the render_template object, and use it in the return of your 
#    function when hitting a specific route
from flask import Blueprint, render_template

# 1. current_user will be used to detect if a user is logged in or not.
# 2. Current_user gives us access to a bunch of attributes, if they are logged in. Like name, email, etc
# 3. If the user is not logged in, it returns to us what is called an anonymous user who is not authenticated.
# 4. When we pass current_user as an argument in the render_template funciton, this means we will be able to
#    reference the current user. If the person is logged in, they will have access to the home page, otherwise blocked
#    by the @log_required.  
# 5.  
from flask_login import login_required, current_user

# 1. Should name the blueprint the same name as the file for ease of use
views = Blueprint('views', __name__)

# 1. Define a view(route)
# 2. The argument is the URL/endpoint we want to use and below is the function we bind to it.
# 3. The return value of the function is what is shown in the browser when we hit the 
#    endpoint/route we passed.
# 4. We register the blueprints in the __init_.py. This tells the app we have blueprints that
#    contain different views/URLs/endpoint for our app and where they are
@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)