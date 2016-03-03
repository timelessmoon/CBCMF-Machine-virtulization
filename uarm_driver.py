from __future__ import division
import serial
import time
import csv
import threading
import json
import ast



class _uarm_driver:

	def __init__(self):

		self.isrunning=False
		self.row_count=0
		#self.reader=None
		self.currentrows=0
		self.totalrows = 0
		self.list_title=None
		self.Uarm_busy=False
		self.completed_percent=0.00
		self.port= None
		self.ser=None
		self.write_data=None
		self.read_function=None

		self.motor_angles=[0,0,0,0,0]

		self.Rotation=0
		self.Y_position=0
		self.Height=0
		self.HandRot=0
		self.Grab=0

	def write_status(self,content):
		

	def set_port(self,setport):

		self.port=setport
		self.ser = serial.Serial(self.port, 9600)
		self.test_port()
		self.init_the_position()

	def get_position(self,_posX, _posY, _posZ, _posHR, Grab):
			
		print "Rotation: " , _posX , "  Y_position: " , _posY , "  Height: " , _posZ , "  HandRot: " , _posHR , "  Grab: " , Grab

		self.Rotation=_posX
		self.Y_position=_posY
		self.Height=_posZ
		self.HandRot=_posHR
		self.Grab=Grab
		position = bytearray([0xFF,
							0xAA,	
							(_posX >> 8) & 0xFF,	#positionX
							_posX & 0xFF,
							(_posY >> 8) & 0xFF,	#positionY
							_posY & 0xFF,
							(_posZ  >> 8) & 0xFF,	#positionH
							_posZ  & 0xFF,
							(_posHR >> 8) & 0xFF,	#Grab_rotation
							_posHR & 0xFF,
							Grab])
		return position
		

	def init_the_position(self):

		if (self.isrunning):
			self.ser.write(self.get_position(0,0,0,0,0x02))

			print ' finish init the position '

	def test_port(self):

		if self.ser.isOpen():
	 		print ' COM3 is redeay to go'
	 		self.isrunning=True
	 	else:
	 		print ' The serial port is incorrect or not opened'

	def check_csv_length(self,file_read):

		self.countrdr = csv.DictReader(file_read)
		for row in self.countrdr:
			self.totalrows += 1
		file_read.seek(0)
		if self.totalrows >= 2:
			return True
		else:
			return False

	def percentage(self):

		self.completed_percent = "{0:.0f}%".format(float(self.currentrows-1)/(self.totalrows+1) * 100)


	def reading_positions(self):
	
		self.motor_angles[0]=self.Rotation
		self.motor_angles[1]=self.Y_position
		self.motor_angles[2]=self.Height
		self.motor_angles[3]=self.HandRot
		self.motor_angles[4]=self.Grab
		

	def arm_write(self,path='positions.csv'):

		with open(path) as f:

			if self.check_csv_length(f) and self.Uarm_busy != True:

				print "files is ready, remains ", self.totalrows ," rows"
				myreader = csv.DictReader(f)

				for line in f:
					self.currentrows+=1

					if (self.currentrows==1 and self.Uarm_busy != True):
						self.currentrows+=1
						self.Uarm_busy=True
					else: 
						lis=line.split(',')	
						self.ser.write(self.get_position(int(lis[0]),int(lis[1]),int(lis[2]),int(lis[3]),int(lis[4])))
						time.sleep(0.1)
						self.percentage()
						self.reading_positions()
						print 'current rows: ', self.currentrows, self.completed_percent
				else:

					f.close()
					self.Uarm_busy=False
					self.completed_percent=0.0
					print 'file loaded ended'

			else:
				print 'the file is empty or Uarm is busy'


	# def adapter_arm_write(self):

	# 	self.write_data=threading.Thread(name='arm_write',target=self.arm_write)
	# 	print 'I am here'
	# 	# self.write_data.start()




	# def adapter_reading_status(self):

	# 	self.read_function=threading.Thread(name='arm_reading_position',target=self.reading_positions)

		# self.reading_positions.start()


if __name__ == '__main__':
	test=_uarm_driver()
	test.set_port('COM3')
	# time.sleep(1)
	# test.arm_write('positions.csv')

	# test.adapter_arm_write('positions.csv')
	# test.write_data.start()
	# test.read_function.start()

	time.sleep(1)
	
	t1=threading.Thread(name='arm_write',target=test.arm_write)
	t2=threading.Thread(name='arm_read',target=test.reading_positions)
	t1.start()
	t2.start()
	