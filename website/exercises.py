# 1. This is a blueprint of our application; it has a bunch of routes/URLs defined inside of it.
from flask import Blueprint, render_template
from flask_login import login_required, current_user

import cv2
import mediapipe as mp
import numpy as np

# 1. gives us all of our drawing utilities. When it comes to visualizing our poses, we will use the drawing utils
mp_drawing = mp.solutions.drawing_utils
# 2. this imports our pose estimation models
mp_pose = mp.solutions.pose

# 1. Should name the blueprint the same name as the file for ease of use
exercises = Blueprint('exercises', __name__)

# ALL EXERCISES

# legs
@exercises.route('/exercises/squats/back_squat_side')
@login_required
def back_squat_side():
    return render_template("/exercises/squats/back_squat_side.html", user=current_user)

# Back
@exercises.route('/exercises/rows/barbell_row_side')
@login_required
def barbell_row_side():
    return render_template("/exercises/rows/barbell_row_side.html", user=current_user)