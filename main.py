# Whenever you put the __init__.py file inside a dir, the dir (website) becomes a python package
# When you import the name of the dir (website) like below, by default it will run all the stuff in the __init__.py
# This means we can import what we define in our __init__.py, like our create_app b/c it will have been ran

from website import create_app

app = create_app()

# Only if we run/execute THIS file directly(main.py), NOT if we import it like we could in a diff file, should we
# execute the app.run line. We only want to run our app if we start it from this file.

# If you were to import main.py from another file and you did not have the __name__ == '__main__', it would
# run the webserver because it's been imported and by default, __init__.py runs

# Debug = True reruns the webserver whenever a change is made. Turn off when in prod
if __name__ == '__main__':
    app.run(debug=True)