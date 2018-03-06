# Network App Design - Final Project 
# Room Density
# Team 07
## Blessy Abeho, Pelin Demir, Hung Nguyen, and Connie Lim

## Description
* This system will monitor the population density of a space.
* The goal is to provide a convenient tracking service that will inform the user about how crowded a space is.
* With this service customers can make informed decisions.
* The system will collect  images with a camera, then use the Rpi to calculate the density of the room. The output will be shown to the customers on an Android app.

# How to run:
* In the Android app repository go to Main_Activity.java and change the IP address in line 69 to the IP address of the machine you are running it on
* Position your RPi camera into one of the desirable configurations: 
* Line-> Google Cloud Cam Server
* Room -> OpenCV/Combination
* Run mongo on your RPi
* Choose the correct server for your RPi's camera configuration and run it using python3
* Run the flask server on the RPi and get the RPi's IP Address through ifconfig
* Now you can run GET request at the IP Address and port (1900) with GET /getData

### Note
* Please run (with the path replaced by the correct path of your authentication file):
```export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/Desktop/share/mhm.json"```


## POSSIBILITIES TO EXPLORE: 
* Can transofrm to a free service
* Crowd, restaurant, offices tracking and monitoring, etc.
* POST requests that can can update the high, medium, low
* Expand to detected emotions. (Are our customers happy? What are their most common emotions during specific times when they come, who are working when they display those emotions?)
* Who are our demographics? Gender, age, etc.?


## Main Tools:
* Google Cloud Vision API
* PiCamera
* MongoDB Aggregates and Analytics
* Flask
* Android App Development 

## Detailed dependencies:
### Python libraries:
pymongo
opencv-python
datetime
imutils
Pillow
google-cloud-vision
picamera

### Web resources:
* https://cloud.google.com/vision/docs/face-tutorial
* https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/vision/cloud-client/face_detection/faces.py
* https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/
* https://www.pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/


### Debug commands for MongoDB
* Journaling DATABASE: sudo mongod --dbpath /var/lib/mongodb/ --journal
* Drop: sudo mongo test --eval "db.dropDatabase();"



