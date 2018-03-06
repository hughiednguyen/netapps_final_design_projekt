#!/usr/bin/env python3

import argparse
import picamera
from time import sleep
from datetime import datetime
import json
from pymongo import MongoClient

from google.cloud import vision
from google.cloud.vision import types


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

    # Camera init and warmup
    camera = picamera.PiCamera()
    sleep(0.5)

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
                print('[{}] Detected {} {}'.format(
                    current_time(), len(faces), 'person' if len(faces) == 1 else 'people')
                    )
                
                # Make json and post to database
                post = {
                    "dt": datetime.now(),
                    "count": len(faces)
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
