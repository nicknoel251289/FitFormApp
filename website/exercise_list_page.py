# 1. This is a blueprint of our application; it has a bunch of routes/URLs defined inside of it.
from flask import Blueprint, render_template
from flask_login import login_required, current_user

# 1. Should name the blueprint the same name as the file for ease of use
exercise_list_page = Blueprint('exercise_list_page', __name__)

# 1. Define a view(route)
# 2. The argument is the URL/endpoint we want to use and below is the function we bind to it.
# 3. The return value of the function is what is shown in the browser when we hit the 
#    endpoint/route we passed.
# 4. We register the blueprints in the __init_.py. This tells the app we have blueprints that
#    contain different views/URLs/endpoint for our app and where they are
# 5. We only have the 1 blueprint, auth, so this will include all the below routes 
@exercise_list_page.route('/exercise_list_page')
@login_required
def exercise():
    return render_template("exercise_list_page.html", user=current_user)
