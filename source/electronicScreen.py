# -*- coding: utf-8 -*-
 
"""
	Shared Ad  Board Dapp on iExec platform
	recomman transfer Image with https://www.file.io/
	-----2019-04-25------
	- Guofeng Shen
	- Add picture changing animation
	-
	-

"""

import sys
from PyQt5.QtWidgets import * # QApplication  ,QWidget 
from PyQt5.QtGui import * # QPixmap,   QPainter 
from PyQt5.QtCore import * #Qt,QThread
#from PyQt5.QtGui import  QtGui
import paho.mqtt.client as mqtt #(# screenID 113217)
import os
import hashlib
import time
import _thread
from PIL import Image
from PIL.ImageQt import ImageQt
import queue
import math
class Winform(QWidget):
	
	def __init__(self,parent=None):
		self.__imagePath__="./defaultImage/1.jpg"
		self.currentImage=[] #always made for paintevent()
		self.lastImage=[]
		self.nextImage=[] 
		self.animationFrameBuffer=queue.Queue() #store animation frames in queue, with PIL image type

		super(Winform,self).__init__(parent)
		self.thread = ControlThread()
		self.setWindowTitle("AdScreen")
		self.setCursor(QCursor(Qt.BlankCursor))

		try:
			self.currentImage = Image.open(self.__imagePath__)
		except Exception as e:
			print(e)
			print('last Image init failed,in Qwidget.__init__()')
		self.lastImage=self.currentImage.copy()
		#timer used in displaying animation
		self.animationDisplayTimer = QTimer()
		self.animationDisplayTimer.timeout.connect(self.displayAnimation)

		#self.setWindowFlags(   Qt.FramelessWindowHint) #freme less
		print(type(self.currentImage))
		self.thread.sinOut.connect(self.setImage)
		self.thread.start()
		self.showFullScreen()
		'''
		self.mqttComThread=MqttComThread()
		self.mqttComThread.sinOut.connect(self.thread.addCustomAd)
		self.mqttComThread.start()
		'''
    #called when form has changed, or force trigger using self.update()\
	#read and display self.currentImage. has to transfer PIL image to QPixmap.
	def paintEvent(self,event): 
		painter = QPainter(self)
		#transfer  PIL image to Qpixmap
		imageq = ImageQt(self.currentImage)
		qimage = QImage(imageq)
		pixmap=QPixmap(qimage)

		#pixmap = QPixmap(self.__imagePath__)
		
	 	#绘制窗口背景，平铺到整个窗口，随着窗口改变而改变
		painter.drawPixmap(self.rect(),pixmap) 


	#animation effect duing image switching, input list of frames in QPixmap's instance
	def tranferAnimation(self,pixmapList): 
		painter = QPainter(self)
		for frame in pixmapList:
			try:
				
				painter.drawPixmap(self.rect(),frame)
				#self.sleep(0.1)
			except expression as identifier:
				print('Error in switching animation')
				print(identifier)
			

	# use [self.lastImage] and [self.nextImage], to  generate a Transition animation frame, store in [animationFrameBuffer]
	def animationGenerator(self):
		self.animationFrameBuffer.queue.clear() #empty the buffer
		framesNum=20
		for i in range(1,framesNum+1):
			i = (math.sin( math.pi/framesNum*i-math.pi/2.0)+1)/2
			print(i)
			imageTemp = Image.blend(self.lastImage,self.nextImage, i)

			self.animationFrameBuffer.put(imageTemp) #put to queue



	def displayAnimation(self):
		if not self.animationFrameBuffer.empty():
			
			#get one frame and send to currentImage, update
			self.currentImage=self.animationFrameBuffer.get()
			self.update()
		else:
			self.animationDisplayTimer.stop()
			# #stop the timer


	def setImage(self,newFile):
		self.__imagePath__=newFile
		#readin next image to be displayed
		try:
			self.nextImage = Image.open(self.__imagePath__)
		except Exception as e:
			print(e)
			print('open current image fail, in setImage()')

		#generate animation frames and start animation timer 
		self.animationGenerator()
		self.animationDisplayTimer.start(30)
		#start timer

			
		'''
		# generate animation
			# 1,self.lastImage is always ready

			# 2, open this time image,
		try:
			self.thisImage = Image.open(self.__imagePath__)
			print('opened this image')
		except Exception as e:
			print(str(e))
			print('Error in SetImage(), open image failed.')
			self.update() # if fail to open this time image, jump over animation

			#3, generate frames of animatiom
		tempPixmapList=[]
		for i in range(1,6):
			imageTemp = Image.blend(self.lastImage,self.thisImage, i/6.0)
			imageTemp = ImageQt(imageTemp)
			imageTemp=QPixmap.fromImage(imageTemp)
			tempPixmapList.append(imageTemp)

			#4,call to display the animation
		self.tranferAnimation(tempPixmapList)

			#5.set this image as lastImage
		self.lastImage=self.thisImage
		'''
		#animation finished, dispaly next image

		# show animate
		pass


		# show next image
		print('setImage'+newFile)
		self.lastImage=self.nextImage.copy()
		#self.update()



class ControlThread(QThread):
	sinOut = pyqtSignal(str)
	
	def __init__(self,parent=None):
		super(ControlThread,self).__init__(parent)
		self.working = True
		self.paiedAdValide = False
		self.adHereImageCount = 1
		self.customAdList=[]# store ad info: {"fileName":'1234',"timeout":0} for i in range(10)]
		self.currentAdIndex=0

		self.mqttObject=MqttComThread()
		self.mqttObject.sinOut.connect(self.addCustomAd)
		self.mqttObject.start()

		#self.num = 0
		
	def __del__(self):
		self.working = False
		self.wait()
	def defaultAd_show(self):
		self.adHereImageCount=self.adHereImageCount+1
		if self.adHereImageCount>2:
			self.adHereImageCount=1
		filepath="./defaultImage/{count}.jpg".format(count=str(self.adHereImageCount))
		# 发出信号		
		self.sinOut.emit(filepath)

	def customAd_show(self):
		filepath='./customImage/'+self.customAdList[self.currentAdIndex]["fileName"]
		self.customAdList[self.currentAdIndex]["timeout"]=self.customAdList[self.currentAdIndex]["timeout"]-1 #该广告剩余时间-1
		
		if self.customAdList[self.currentAdIndex]["timeout"]==0: #如果该广告时间到期
			#从列表中删除
			cmd='rm -f '+ './customImage/'+self.customAdList[self.currentAdIndex]["fileName"]
			del self.customAdList[self.currentAdIndex]
			os.system(cmd)
			if len(self.customAdList)==0: #判断客户广告队列是否已空
				self.paiedAdValide = False
			return

		self.currentAdIndex=self.currentAdIndex+1 #广告播放序号+1
		if self.currentAdIndex>=len(self.customAdList): #下标越界之后扳回
			self.currentAdIndex=0

		# 发出更新信号		
		self.sinOut.emit(filepath)

	def addCustomAd(self,newAdUrl):
		#插入新客户广告，由通信信号驱动
		print("receved message:"+str(newAdUrl))
		md5 = hashlib.md5() #利用时间hash值作为文件名
		md5.update(str(time.time()).encode('utf8'))
		fileName=md5.hexdigest()+'.jpg'
		cmdTemp='curl -o ./customImage/' +  fileName +' ' +str(newAdUrl) #download Ad image and rename
		stateCode=os.system(cmdTemp)
		if stateCode == 0: # if curl download succeed.
			#merge customed image into ad template, and transfor into jpeg format. 
			try:
				#im=Image.open('/home/gf/ElectronicScreen/dist/electronicScreen/customImage/'+fileName)
				im=Image.open('./customImage/'+fileName)
			except Exception as e:
				print(str(e))
				print('Image open failed, will be ignored.')
				return
			im_template=Image.open('./defaultImage/template.jpg')
			adRegionBox=(64,32,1606,999)
			im_template.paste(im.resize((1542,967),Image.BICUBIC),adRegionBox)
			im_template.save('./customImage/'+fileName)
			# image process ended, add to customAdList. 
			self.customAdList.append( {"fileName":fileName,"timeout":20})
			self.paiedAdValide = True
			print("addCustomAd,URL:"+str(newAdUrl))
		else:
			print("Invalid message. Ignored.")
			


	def run(self):
		while self.working == True:
			
			#self.num += 1	
	
			self.sleep(6)
			if self.paiedAdValide==False:
				self.defaultAd_show()
			else:
				self.customAd_show()
				#showCustomAd				
				pass		
			#self.sinOut.emit('./image/2.jpg')
			#print('tick')

class MqttComThread(QThread):
	#通过mqtt协议与Dapp通讯，在Control类中实例化
	sinOut = pyqtSignal(str)
	
	def __init__(self,parent=None):
		super(MqttComThread,self).__init__(parent)
		self.working = True

		self.HOST = "broker.hivemq.com" #"test.mosquitto.org" 
		self.PORT = 1883
		self.client = mqtt.Client()
		

 
	def __del__(self):
		self.working = False
		self.wait()
 
	def on_connect(self, mqttc, obj, flags, rc):
		print("Connected with result code "+str(rc))
		

	def on_message(self, mqttc, obj, msg):
		print(msg.topic+" " + ":" + str(msg.payload))
		self.sinOut.emit(msg.payload.decode('utf-8'))

	#def subscribe(self):
		
	def mqttloop():
		self.client.loop()
		print('MQTT module tick')
		
	def run(self):
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.connect(self.HOST, self.PORT, 60)
		self.client.subscribe("SHIFT_AdScreen113217")
		
		self.client.loop_forever()
		'''
		while self.working == True:
			
			#self.num += 1	
			self.client.loop_start()
			self.sleep(5)
			
			#self.sinOut.emit('./image/2.jpg')
			print('MQTT module tick')
		'''

'''
class MqttComThreadTest(QObject):
	#通过mqtt协议与Dapp通讯，在Control类中实例化
	#sinOut = pyqtSignal(str)
	sinOut = pyqtSignal(str)
	def __init__(self,parent=None ):
		super( ).__init__(parent)
		self.working = True

		self.HOST = "test.mosquitto.org" 
		self.PORT = 1883
		self.client = mqtt.Client()
		

 
	def on_connect(self, mqttc, obj, flags, rc):
		print("Connected with result code "+str(rc))
		

	def on_message(self, mqttc, obj, msg):
		print(msg.topic+" " + ":" + str(msg.payload))
		self.sinOut.emit(str(msg.payload))

	#def subscribe(self):
		


		
	def run(self):
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.connect(self.HOST, self.PORT, 60)
		self.client.subscribe("SHIFT_AdScreen113217", 0)
		self.client.loop_start()
		self.client.loop_forever()
		while self.working == True:
			
			#self.num += 1	
	
			time.sleep(5)
			
			#self.sinOut.emit('./image/2.jpg')
			print('MQTT module tick')

'''




if __name__ == "__main__":  
		
		app = QApplication(sys.argv) 
		form = Winform()
		form.show()
		
		# mqtt.connect() would cause Segmentation fault
		# after tried to fix , but failed, I decide to start free riding NOW
		'''
		HOST = "test.mosquitto.org" 
		PORT = 1883
		client = mqtt.Client()
		

 
		def on_connect(client, userdata, flags, rc):
			print("Connected with result code "+str(rc))
		

		def on_message(client, userdata, msg):
			print(msg.topic+" " + ":" + str(msg.payload))
			#self.sinOut.emit(str(msg.payload))
			form.thread.addCustomAd(msg.payload)
			
		client.on_connect = on_connect
		client.on_message = on_message
		client.connect( HOST,  PORT, 60)
		client.subscribe("SHIFT_AdScreen113217", 0)
		#client.loop_forever()
		def mqttLoopThread():
			client.loop_forever()

		_thread.start_new_thread(mqttLoopThread,())
		'''

		'''
		mqtt=MqttComThreadTest()
		mqtt.sinOut.connect(form.thread.addCustomAd)
		mqtt.run()
		'''
		sys.exit(app.exec_())
