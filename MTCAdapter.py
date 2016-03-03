"""
author: Kent Vasko
company: MAYA Design
"""

import sys

from second_Uarm_adapter import *
# For keeping snapshots of the machine states (sequences).
import copy
import traceback

# @class: MTCAdapter
class MTCAdapter:
    # @function: init
    def __init__(self, adapterType):
        # Initialze adapter as null.
        self.adapter = None
        # If the adapter is for a Makerbot.
        if adapterType == "Uarm":
            # Set this adapter to be a makerbot adapter.
            self.adapter = UarmAdapter()
        # end if MakerbotAdapter
    # end init
    
    # @function: pollDevice
    def pollDevice(self):
        # Return data from the specific adapter's pollDevice function.
        c=self.adapter.pollDevice()
        print "I am here"
        print c
        return c

    # end pollDevice
    
# end MTCAdapter
