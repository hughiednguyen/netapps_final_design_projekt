#!/usr/bin/env python3

import argparse
import picamera.array
import picamera
from time import sleep
from datetime import datetime
import json
from pymongo import MongoClient

from google.cloud import vision
from google.cloud.vision import types

from imutils.object_detection import non_max_suppression
from imutils import paths
import cv2
import numpy as np
import imutils


def detect_face(client, face_file, max_results=999):
    content = face_file.read()
    image = types.Image(content=content)

    return client.face_detection(image=image).face_annotations


def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def main():
    # MongoDB init
    database_client = MongoClient()
    database = database_client.test
    collection = database['team7']

    # Cloud API Client init
    client = vision.ImageAnnotatorClient()

    # Camera init
    camera = picamera.PiCamera()

    # initialize the HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Run a label request on a single image every time it finishes
    # Post the count to our mongodb with timestamp and count
    try:
        print('[{}] -----STARTING SERVER-----'.format(current_time()))

        camera.start_preview()
        while(True):
            # Capture image
            camera.capture('image.jpg')

            with open('image.jpg', 'rb') as image:
                
                # Send request with image to Cloud Vision API
                faces = detect_face(client, image, 9999)

                # Prints out the face count
                print('[{}] Detected {} face{}'.format(
                    current_time(), len(faces), '' if len(faces) == 1 else 's')
                    )
                
                # OpenCV processing
                cv_image = cv2.imread('image.jpg')
                
                max_body_count = 0

                # Detect people in the image
                (rects, weights) = hog.detectMultiScale(cv_image, winStride=(4, 4), padding=(8, 8), scale=1.05)

                # Apply non-maxima suppression to the bounding boxes using a
                # fairly large overlap threshold to try to maintain overlapping
                # boxes that are still people
                rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
                pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

                # Show some information on the number of dectections
                print("[{}] {} bod{} without suppression, {} bod{} after suppression".format(
                    current_time(),
                    len(rects),
                    'y' if len(rects) == 1 else 'ies',
                    len(pick),
                    'y' if len(pick) == 1 else 'ies'))

                # Pick the highest count to accomdate for bodies without faces
                max_body_count = max(len(faces), len(pick))

                # Make json and post to database
                post = {
                    "dt": datetime.now(),
                    "count": max_body_count
                    }

                collection.insert_one(post)
    except:
        camera.stop_preview()
        camera.close()
    finally:
        camera.stop_preview()
        camera.close()

if __name__ == '__main__':
    main()
