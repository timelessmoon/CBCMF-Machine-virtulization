"""
author: Kent Vasko
company: MAYA Design
"""


import json
import ast
import time

port='/dev/ttyUSB1'

# @class: UarmAdapter
class UarmAdapter:
    # @function: init
    def __init__(self):
        # Instance variables.
        self.available = True

        self.Data={}
    # end init
    
    def pollDevice(self,Uport=port):
        # Structure to hold data.
        Uarm_Data = {"availability":"UNAVAILABLE","Connection":"OFFLINE",
                        "xPos":"UNAVAILABLE","yPos":"UNAVAILABLE","zPos":"UNAVAILABLE",
                        "Grabber":"UNAVAILABLE","Grab_rotation":"UNAVAILABLE",
                         "Progresspercentage":"00.0%"
                        }

        UarmPort=Uport
        
        # If the Uarm was found.
        if UarmPort != None:
            # Get values from the Uarm.
            try:
                f=open('test-write.txt','r')
                s=f.read()
                whip=ast.literal_eval(s)
                Uarm_Data=whip
                f.close()
            except:
                print "MakerbotAdapter.pollMakerbot, Error getting data from Makerbot: "
            # end try-catch
        # end if
        # Otherwise, set things accordingly.
        else:
            self.available = False
        # end else
        
        # Return the reslts.
        print Uarm_Data
        return Uarm_Data
    # end pollDevice

    # @function: setAvailability
    def setAvailability(self, availability):
        self.available = availability
    # end setAvailability
    
    # @function: isAvailable
    def isAvailable(self):
        return self.available
    # end isAvailable
# end MakerbotAdapter



if __name__ == '__main__':
    test=UarmAdapter()
    data={}
    data=test.pollDevice()
    print data
