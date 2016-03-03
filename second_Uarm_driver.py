from __future__ import division
import serial
import time
import csv
import threading
import json
import ast
import socket
import select



class _uarm_driver:

        def __init__(self):
                self.Uarm_Data = {"availability":"UNAVAILABLE","Connection":"OFFLINE",
                        "xPos":"UNAVAILABLE","yPos":"UNAVAILABLE","zPos":"UNAVAILABLE",
                        "Grabber":"UNAVAILABLE","Grab_rotation":"UNAVAILABLE",
                         "Progresspercentage":"00.0%"
                        }
                self.isrunning=False
                self.row_count=0
                self.currentrows=0
                self.totalrows = 0
                self.list_title=None
                self.Uarm_busy=False
                self.completed_percent=0.00
                self.port= None
                self.ser=None
                self.write_data=None
                self.read_function=None
                self.f=None


        def init_write_status(self):

                self.f=open('test-write.txt','wb')

        def write_status(self):

                self.init_write_status()
                json.dump(self.Uarm_Data,self.f)
                # json.dump('\r',self.f)
                self.f.close()
                time.sleep(0.02)

        def set_port(self,setport):

                self.port=setport
                self.ser = serial.Serial(self.port, 9600)
                self.test_port()
                self.init_the_position()

        def get_position(self,_posX, _posY, _posZ, _posHR, Grab):
                        
                print "Rotation: " , _posX , "  Y_position: " , _posY , "  Height: " , _posZ , "  HandRot: " , _posHR , "  Grab: " , Grab

                self.Uarm_Data["xPos"]=str(_posX)
                self.Uarm_Data["yPos"]=str(_posY)
                self.Uarm_Data["zPos"]=str(_posZ)
                self.Uarm_Data["Grabber"]=str(Grab)
                self.Uarm_Data["Grab_rotation"]=str(_posHR)

                position = bytearray([0xFF,
                                                        0xAA,   
                                                        (_posX >> 8) & 0xFF,    #positionX
                                                        _posX & 0xFF,
                                                        (_posY >> 8) & 0xFF,    #positionY
                                                        _posY & 0xFF,
                                                        (_posZ  >> 8) & 0xFF,   #positionH
                                                        _posZ  & 0xFF,
                                                        (_posHR >> 8) & 0xFF,   #Grab_rotation
                                                        _posHR & 0xFF,
                                                        Grab])
                return position
                

        def init_the_position(self):

                self.ser.write(self.get_position(0,0,0,0,0x02))
                self.Uarm_Data["availability"]="available"
                print ' finish init the position '
                self.write_status()

        def test_port(self):

                if self.ser.isOpen():
                        print ' COM3 is redeay to go'
                        self.isrunning=True
                        self.Uarm_Data["Connection"]="Online"
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
                self.Uarm_Data["Progresspercentage"]=str(self.completed_percent)
                self.Uarm_Data["availability"]="BUSY"

        def arm_write(self,path='current_movement.csv'):

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
                                                print 'current rows: ', self.currentrows, self.completed_percent
                                        
                                                self.write_status()
                                                
                                else:

                                        f.close()
                                        self.Uarm_Data["availability"]="available"
                                        self.f.close
                                        self.Uarm_busy=False
                                        self.completed_percent=0.0
                                        self.isrunning=False
                                        self.write_status()
                                        print 'file loaded ended'

                        else:
                                print 'the file is empty or Uarm is busy'





if __name__ == '__main__':
    test=_uarm_driver()
    test.set_port('/dev/ttyUSB1')


    time.sleep(1)
    
    # t1=threading.Thread(name='arm_write',target=test.arm_write)
    # t2=threading.Thread(name='arm_read',target=test.write_status)
    # t2.start()

    s = socket.socket()#initial the socket        
    host = '131.151.113.215'# ip of raspberry pi 
    print("Socket successfully created")
    port = 12345#port
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))#bind the socket to the ip address
    print("socket binded")
    command = ""
    s.listen(5)
    print("socket is listening")        
    s.setblocking(0)
        
    while True:
        try:
            # strat to write status into the XML file
            ready = select.select([s],[],[],0.5)#save the speaker's ip address for future 
            if ready[0]:
                c, addr = s.accept()     
                print ('Got connection from', addr)
                #data = input("Enter data to be sent: ")
                #send a thank you message to the client. 
                #c.send(("Thank you for connecting").encode('utf-8'))
                try:
                    command = (c.recv(1024)).decode('utf-8')
                    print command
                    print " Command received. Processing ..."
                    if ("load" in command):
                        #file = command.split()
                        #print file
                        #fileName = "/home/pi/MyApp/" + file[1]
                        #print fileName
                        f = open('/home/pi/testforsocket/current_movement.csv','wb')
                        #f = open('/home/pi/MyApp/current_print.stl','wb')
                        c.send('1')#ready to receive
                        #cs, addr = s.accept()
                        time.sleep(1)
                        l = c.recv(1024)
                        while (l) :
                            print "receiving..."
                            f.write(l)
                            l = c.recv(1024)
                            #print l
                        f.close()
                        print "Done receiving."
                        time.sleep(1)
                        test.arm_write()

                    elif("reset" in command):

                        test.init_the_position()
                        
                except Exception, exc:
                    print exc

        except KeyboardInterrupt:   
            s.close()
            print "Connection terminated. Thank you."   
            sys.exit()  
        except socket.error,select.error:
            s.close()
            s = socket.socket()        
            host = '130.184.104.182'# ip of raspberry pi 
            print("Socket successfully created")
            port = 12345
            s.bind((host,port))
            print("socket binded")
            s.listen(5)
            print("socket is listening")
            s.setblocking(0)
            
