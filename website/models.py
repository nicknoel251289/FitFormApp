# 1. import from the current package, the website dir, the db object (from init.py)
# 2. the '.' is the same as sayung 'from website import db'
from . import db
# 1:17:10 in vid
from flask_login import UserMixin
from sqlalchemy import func

# 1. User inherits from db.Model and UserMixin. UserMixin helps with login authentication
# 2. a db model is a blueprint for an object that's going to be stored in your DB. So for
#    users, this means all users must conform to the model/blueprint.
# 3. By default, when you add a new object, you do not need to define its ID, it will 
#    automatically be set for you. It's smart enough to increment the IDs
# 6. To allow users to find their notes, we need to set up a field in our User class. 
#    This will tell Flask and SQLAlchemy that everytime we create a note, add into this 
#    users notes relationship, that note ID. 
# 7. Under the hood, it must know to use the primary_key. 
# 8. You do need a capital for the db.relationship argument
# 9. UserMixin allows it so that we can use the 'current_user' object in auth.py to access all the info about
#    the currently logged in user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

# 1. func.now() is the same as datetime.now
# 2. How we assocciate different information with different users is by a foreign key.
# 3. A foreign key is a key on one of the tables in your DB that always references a
#    a column in another table in the DB.
# 4. In this example, we want to always store the user who created the note. We can do
#    this by passing the db method, ForeignKey and the argument 'user.id'
# 5. In python we use uppercase for classes as a naming convention, but the 'user.id'
#    is just referencing the User class.

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Back_Squat_Side(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))