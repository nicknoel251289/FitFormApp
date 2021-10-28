# 1. This is a blueprint of our application; it has a bunch of routes/URLs defined inside of it.
from flask import Blueprint, render_template, Response, request
from flask.helpers import url_for
from flask_login import login_required, current_user, utils

import cv2
from imutils import video
import mediapipe as mp
import numpy as np
from imutils.video import VideoStream
import imutils
import time
import datetime
from threading import Thread

# 1. gives us all of our drawing utilities. When it comes to visualizing our poses, we will use the drawing utils
mp_drawing = mp.solutions.drawing_utils
# 2. this imports our pose estimation models
mp_pose = mp.solutions.pose

class set_exercise:
    current_exercise = None
    current_angle = None

# 1. Should name the blueprint the same name as the file for ease of use.
exercises = Blueprint('exercises', __name__)

class VideoCamera(object):

    def __init__(self):
        self.stream = cv2.VideoCapture(0)

    def __del__(self):
        self.stream.release()

    def get_frame(self, exercise):
        
        success, frame = self.stream.read()

        # 1. .Pose access our pose estiamtion models
        # 2. min_detection_confidence is what we want our detection confidence to be
        # 3. min_tracking_confidence is what we want our tracking confidence to be, when we maintain our state
        # 4. If we want to be more accurate, increase the metrics to .8 or .95. There is a tradeoff with increasing
        #    these numbers. It will require a more persize pose from the person which could be more difficult
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # make detection
            results = pose.process(image)

            # Recolor back to BGR (BGR NOT RGB)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # exercise to calculate angle for
                poi_coord, angle = exercise_to_calc(exercise, landmarks, image)

                # vizualize
                # str(angle) - turn our angle into a string
                # Tuple(....astype()) The coordinates we get by default are normalized and not adjust for the cameras dimensions.
                #     This allows us to find the correct coordinates within our cameras dimensions 
                cv2.putText(image, str(angle), tuple(np.multiply(poi_coord, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            except:
                pass

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                        )


        success, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def generate_camera(video_camera, current_exercise):
    while True:
        frame = video_camera.get_frame(current_exercise)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@exercises.route('/video_feed')
@login_required
def video_feed():
    print(set_exercise.current_exercise)
    return Response(generate_camera(VideoCamera(), set_exercise.current_exercise), mimetype='multipart/x-mixed-replace; boundary=frame')

@exercises.route('/record', methods=['GET'])
@login_required
def record():
    print("TEST")
    return Response("test")

# EXERCISES
# legs
@exercises.route('/exercises/squats/back_squat_side')
@login_required
def back_squat_side():
    set_exercise.current_exercise = 'back_squat_side'
    return render_template("/exercises/squats/back_squat_side.html", user=current_user)
    #return render_template("/exercises/squats/back_squat_side.html", user=current_user)

# Back
@exercises.route('/exercises/rows/barbell_row_side')
@login_required
def barbell_row_side():
    set_exercise.current_exercise = 'barbell_row_side'
    return render_template("/exercises/rows/barbell_row_side.html", user=current_user, angle=set_exercise.current_angle)

# get the points on which we want to calculate our angle
def exercise_to_calc(exercise, landmarks, image):
    if(exercise == 'barbell_row_side'):
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        angle = calc_angle(shoulder, elbow, wrist)
        set_exercise.current_angle = angle
        return elbow, angle

# CALC ANGLE
def calc_angle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle