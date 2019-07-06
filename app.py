from flask import Flask, request, abort
from subprocess import call

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json

import errno
import os
import sys, random
import tempfile
import time
import datetime

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)
from picamera import PiCamera
camera = PiCamera()
camera.resolution = (640,480)

x = True
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)
app = Flask(__name__)
app = Flask(__name__, static_url_path = "/coba", static_folder = "coba")
# Channel Access Token
line_bot_api = LineBotApi('DLKJqrx5Yc1E56V/+yW8kQ/d2ZuO9ZA4TvbVc7j035VdBz7FuKvt8IH0HVF48tZpa1bx2uXR8vM3/XMfcl4kpjBDy8smRcy6m0uSNwR3xC1DpbFxahcixD2c4JcngMySfKPFhefecAp4/j64AwxZJwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('f91475fe556eb7fa6c40b48327a9f5e1')
#===========[ NOTE SAVER ]=======================
notes = {}

def take_photo():
	data= datetime.datetime.now().strftime("%Y:%m:%D:%H:%M:%S")
	camera.start_preview()
	time.sleep(5)
	camera.capture('coba/image.jpg')
	camera.stop_preview()
	image1 ="/home/pi/Downloads/nadyalulussekarang/coba/image.jpg"
	image2 ="/home/pi/Downloads/nadyalulussekarang/coba/image1.jpg"
	call(["convert",image1, "-resize", "320x240",image2])
	time.sleep(2)
def take_video():
	data= time.strftime("%d_%b_%Y\%H:%M:%S:%f")
	camera.start_preview()
	camera.start_recording('coba/rec.H264')
	time.sleep(5)
	camera.stop_recording()
	camera.stop_preview()
	video1 ="/home/pi/Downloads/nadyalulussekarang/coba/rec.H264"
	video2 ="/home/pi/Downloads/nadyalulussekarang/coba/rec.mp4"
	call(["rm",video2])
	call(["MP4Box", "-add", video1,video2])
	time.sleep(2)
def alat(x):
	yx=0
	while x == True:
		i=GPIO.input(11)
		if i==0:
			print(i)
			time.sleep(2)
			yx=0
		elif i==1:
			print("Motion Detect")
			yx = yx + 1
			if yx==3:
				x = False
				line_bot_api.broadcast(TextSendMessage(text='Motion Detect'))
				line_bot_api.broadcast(TextSendMessage(text='Type "Menu" Or "Next" For Ignore '))
				take_photo()
				take_video()

			#print(send_message())
			time.sleep(2)


alat(x)
# Post Request
@app.route("/callback", methods=['POST'])
def callback():
	signature = request.headers['X-Line-Signature']
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	try:
	    handler.handle(body, signature)
	except InvalidSignatureError:
	    abort(400)
	return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get user_id
    gid = event.source.sender_id #get group_id
#=====[ TEMPLATE MESSAGE ]=============
    if text == 'Menu':
        buttons_template = TemplateSendMessage(
            alt_text='template',
            template=ButtonsTemplate(
                title='Menu',
                text= 'Choose One Of The Menu',
                actions=[
                    MessageTemplateAction(
                        label='Take Video',
                        text='TakeVideo'
                    ),
                    MessageTemplateAction(
                        label='Take Foto',
                        text='TakeFoto'
                    )
                ]
            )
        )
        print(event.reply_token)
        line_bot_api.reply_message(event.reply_token, buttons_template)

    elif text == 'TakeFoto':
        line_bot_api.push_message(sender, TextSendMessage(text='Image Captured Successfully'))
        data= datetime.datetime.now().strftime("%Y:%m:%D:%H:%M:%S:%f")
        line_bot_api.push_message(sender, TextSendMessage(text='at : '+data))
	#take_photo()
        time.sleep(1)
        message = ImageSendMessage(
          original_content_url='https://nadya.serveo.net/coba/image.jpg',
          preview_image_url='https://nadya.serveo.net/coba/image1.jpg')
        line_bot_api.reply_message(event.reply_token,message)
        print(event.reply_token)
        data= datetime.datetime.now().strftime("%Y:%m:%D:%H:%M:%S:%f")
        line_bot_api.push_message(sender, TextSendMessage(text='at : '+data))
        time.sleep(5)
        try:
           line_bot_api.push_message(sender, TextSendMessage(text='Type "Next" For Detecting Motion'))
        except LineBotApiError as e:
           abort(400)
    elif text == 'TakeVideo':
        line_bot_api.push_message(sender, TextSendMessage(text='Video Recorded Successfully'))
        data= datetime.datetime.now().strftime("%Y:%m:%D:%H:%M:%S:%f")
        line_bot_api.push_message(sender, TextSendMessage(text='at : '+data))
	#take_photo()
        time.sleep(1)
        message = VideoSendMessage(
   	  original_content_url='https://nadya.serveo.net/coba/rec.mp4',
    	  preview_image_url='https://nadya.serveo.net/coba/image1.jpg')
        line_bot_api.reply_message(event.reply_token, message)
        data= datetime.datetime.now().strftime("%Y:%m:%D:%H:%M:%S:%f")
        line_bot_api.push_message(sender, TextSendMessage(text='at : '+data))
        time.sleep(5)
        try:
           line_bot_api.push_message(sender, TextSendMessage(text='Type "Next" For Detecting Motion'))
        except LineBotApiError as e:
           abort(400)
    elif text == 'Next':
        x = True
        alat(x)
#=======================================================================================================================
import os


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=port)
