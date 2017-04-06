# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from PIL import Image
import zbar
import lcddriver
import RegisterTime as timer
import Database as fb

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = lcddriver.lcd()
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
 
	# show the frame
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# Converts image to grayscale.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = Image.fromarray(gray)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

        
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

    if(fb.convertTimetoDecimal(timer.currentTime()) >=  fb.convertTimetoDecimal('18:00:00')) & (fb.convertTimetoDecimal(timer.currentTime()) <=  fb.convertTimetoDecimal('18:05:00')) :
        fb.listar()

	# Scans the zbar image.
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)
        
        display.lcd_display_string(timer.currentDate(), 1)
        display.lcd_display_string(fb.currentClass(), 1)
        # Prints data from image.
        for decoded in zbar_image:
                display.lcd_display_string(fb.validarHistoria(decoded.data), 2)
                time.sleep(2)
                display.lcd_clear()
            
