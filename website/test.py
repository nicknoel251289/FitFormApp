# 1. This is a blueprint of our application; it has a bunch of routes/URLs defined inside of it.
from flask import Blueprint, render_template, Response
from flask_login import login_required, current_user

import cv2
import mediapipe as mp
import numpy as np
from imutils.video import VideoStream
import imutils
import time

# 1. gives us all of our drawing utilities. When it comes to visualizing our poses, we will use the drawing utils
mp_drawing = mp.solutions.drawing_utils
# 2. this imports our pose estimation models
mp_pose = mp.solutions.pose


# 1. Should name the blueprint the same name as the file for ease of use.
exercises = Blueprint('exercises', __name__)

class VideoStream(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

                with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:

                    # Recolor image to RGB
                    image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False

                    # make detection
                    results = pose.process(image)

                    # Recolor back to BGR (BGR NOT RGB)
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    # Render detections
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                success, jpeg = cv2.imencode('.jpg', image)
                return jpeg.tobytes()

            time.sleep(.01)


class VideoCamera(object):
    def __init__(self):
        self.stream = cv2.VideoCapture(0)

    def __del__(self):
        self.stream.release()

    def get_frame(self):
        success, frame = self.stream.read()

        # 1. .Pose access our pose estiamtion models
        # 2. min_detection_confidence is what we want our detection confidence to be
        # 3. min_tracking_confidence is what we want our tracking confidence to be, when we maintain our state
        # 4. If we want to be more accurate, increase the metrics to .8 or .95. There is a tradeoff with increasing
        #    these numbers. It will require a more persize pose from the person which could be more difficult
        with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # make detection
            results = pose.process(image)

            # Recolor back to BGR (BGR NOT RGB)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)


        success, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def gen_camera(video_camera):
    while True:
        frame = video_camera.get_frame()
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_stream(video_stream):
    while True:
        frame = video_stream.update()
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# VIDEO/STREAM FEED
@exercises.route('/video_feed')
@login_required
def video_feed():
    return Response(gen_camera(VideoCamera ()), mimetype='multipart/x-mixed-replace; boundary=frame')

@exercises.route('/stream')
@login_required
def stream():
    return Response(generate_stream(VideoStream()), mimetype='multipart/x-mixed-replace; boundary=frame')


#EXERCISES
# legs
@exercises.route('/exercises/squats/back_squat_side')
@login_required
def back_squat_side():
    return render_template("/exercises/squats/back_squat_side.html", user=current_user)
    #return render_template("/exercises/squats/back_squat_side.html", user=current_user)

# Back (index)
@exercises.route('/exercises/rows/barbell_row_side')
@login_required
def barbell_row_side():
    return render_template("/exercises/rows/barbell_row_side.html", user=current_user)


