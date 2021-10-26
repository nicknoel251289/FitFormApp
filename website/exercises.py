# 1. This is a blueprint of our application; it has a bunch of routes/URLs defined inside of it.
from flask import Blueprint, render_template, Response
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

# 1. Should name the blueprint the same name as the file for ease of use.
exercises = Blueprint('exercises', __name__)

class VideoCamera(object):

    def __init__(self):
        self.stream = cv2.VideoCapture(0)

    def __del__(self):
        self.stream.release()

    def get_landmarks(self):
        return self.landmarks

    def get_frame(self):
        
        frame_rate = 120
        prev = 0
        time_elapsed = time.time() - prev

        success, frame = self.stream.read()

        if time_elapsed > 1./frame_rate:
            prev = time.time()

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
                    self.landmarks = landmarks
                except:
                    pass

                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                            mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                            mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                            )


            success, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()

def generate_camera(video_camera, exercise):
    while True:
        frame = video_camera.get_frame()
        landmarks = video_camera.get_landmarks()
    
        exercise_to_calc('barbell_row_side', landmarks)

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@exercises.route('/video_feed')
@login_required
def video_feed():
    return Response(generate_camera(VideoCamera(), 'barbell_row_side'), mimetype='multipart/x-mixed-replace; boundary=frame')

# EXERCISES
# legs
@exercises.route('/exercises/squats/back_squat_side')
@login_required
def back_squat_side():
    return render_template("/exercises/squats/back_squat_side.html", user=current_user)
    #return render_template("/exercises/squats/back_squat_side.html", user=current_user)

# Back
@exercises.route('/exercises/rows/barbell_row_side')
@login_required
def barbell_row_side():
    return render_template("/exercises/rows/barbell_row_side.html", user=current_user)

# get the type of angle we need for specific exercise
def exercise_to_calc(exercise, landmarks):
    if(exercise == 'barbell_row_side'):
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        calc_LeftShoulder_LeftElbow_LeftWrist(shoulder, elbow, wrist)


def calc_LeftShoulder_LeftElbow_LeftWrist(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    print(angle)

    return angle