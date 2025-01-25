#! /usr/bin/python -u

import threading
from picamera2 import Picamera2, Preview, Controls
from libcamera import controls
import time
import os

# This is necessary since exceptions are thrown in different threads
# causing the program to just hang instead of crash
def excepthook(args):
    print(args.exc_type, args.exc_value)
    print("picamera2 failed")
    os._exit(-1)

threading.excepthook = excepthook

cam = Picamera2()
# Ask for a 1920x1080 frame size from the camera
config = cam.create_video_configuration({"size": (1920, 1080)})
cam.align_configuration(config)
cam.configure(config)

# Open up a full screen preview with no x server
cam.start_preview(Preview.DRM, x=0, y=0, width=1920, height=1080)
cam.start()

# Enable auto exposure, white balance, and focus and ask for 30 fps (1000000/33333)
with cam.controls as ctrl:
    ctrl.AeEnable = True
    ctrl.AwbEnable = True
    ctrl.AfMode = controls.AfModeEnum.Continuous
    ctrl.FrameDurationLimits = (33333,33333)

# Loop forever
while True:
    time.sleep(0.05)
