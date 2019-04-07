import os
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

from picamera import PiCamera
camera = PiCamera()
camera.resolution = (640,480)

def take_photo():
        camera.capture('/home/pi/cam.jpg')

def send_message():
        temp = os.popen("curl -X POST https://notify-api.line.me/api/notify -H 'Authorization: Bearer h4A/0EsqXaNhrkUTvd5GrtIle2lu65p0j79t6nEpt70ZBKEUfYBCCzsK9dwv+WIx0TpEM8n9YTrOBcP3ifRfWp/AnqEnTCv/6o/yUAoQNXUsuh7qMSjsVbX5j4i3uP7mS7SanV4kCf9XAJu2zDXT4wdB04t89/1O/w1cDnyilFU= ' -F 'message=Motion Detect' -F 'imageFile=@/home/pi/cam.jpg'").readline()
        return (temp.replace("temp=",""))
while True:         
    i=GPIO.input(11)
    if i==0:
        print(i)
        time.sleep(0.1)
    elif i==1:
        print("Motion Detect")       
        print(take_photo())
        print(send_message())
        time.sleep(0.1)