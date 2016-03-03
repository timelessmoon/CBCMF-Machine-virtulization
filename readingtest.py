# import json
# import ast
# import time

# data={}
# f=open('test-write.txt','r')
# s=f.read()
# whip=ast.literal_eval(s)
# while True:
# 	f=open('test-write.txt','r')
# 	s=f.read()
# 	whip=ast.literal_eval(s)
# 	print whip
# 	time.sleep(0.1)
# 	f.close()

import BaseHTTPServer
import time
from datetime import datetime
#!/usr/bin/python
HOST_NAME = '131.151.115.194'
PORT_NUMBER = 1080

# Load the configuration data for this agent.

""" Webserver classes. """

# @class: MTCAgentHandler
class MTCAgentHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    # end createMTCHook
    # @function: do_HEAD
    def do_HEAD(s):
        # Send a success response.
        s.send_response(200)
        # Send the content type.
        s.send_header("Content-type", "text/xml")
        # End the headers.
        s.end_headers()
    # end do_HEAD
    
    # @function: do_GET
    def do_GET(s):
        # Send the header information (success, content type)
        s.send_response(200)
        s.send_header("Content-type", "text/xml")
        s.end_headers()
        
        try:
            # Split up the path to be easier to parse or analyze.
            splitPath = s.path.split("?")
            # Grab the command, possibly the machine name too.
            command = splitPath[0]

            # Grab the parameters.
            params = None
            if len(splitPath) > 1:
                params = splitPath[1]
            # end if

            # Take off the leading "/".
            command = command.lstrip("/")

            # Device, if specified.
            specifiedDevice = None
            # If the command contains a "/".
            if "/" in command:
                # Split on that character
                splitCommand = command.split("/")
                # The first parameter will be the specified device.
                specifiedDevice = splitCommand[0]
                # The command is the second element.
                command = splitCommand[1]
            # end if

            # If the probe has been requested.
            if command == "probe":
                # Write the data.
                s.wfile.write(agent.deviceEncode())
            # end if probe
            # If current status has been requested.
            elif command == "current":
                # If there is a question mark, then grab the rest of the path for parsing the desired details.
                if params != None:
                    # Grab the other desired details.
                    desiredDetails = s.path[s.path.index("?")+1:]
                    #print "desired details: "+str(desiredDetails)
                    # Write the current desired data.
                    s.wfile.write(agent.currentStreamEncode(deviceName=specifiedDevice, details=desiredDetails))
                # end if
                # If the device is specified in the path.
                elif specifiedDevice != None:
                    # Write the current desired data.
                    s.wfile.write(agent.currentStreamEncode(deviceName=specifiedDevice))
                # end elif
                # Otherwise, just call a generic current request.
                else:
                    # Write all of the current data.
                    s.wfile.write(agent.currentStreamEncode())
                # end if
            # end if current
            # If a sample status has been requested.
            elif command == "sample":
                # If there is a question mark, then grab the rest of the path for parsing the desired details.
                if params != None:
                    # Grab the other desired details.
                    desiredDetails = s.path[s.path.index("?")+1:]
                    
                    # Write the current desired data.
                    result = agent.sampleStreamEncode(deviceName=specifiedDevice, details=desiredDetails)
                    #s.wfile.write(agent.sampleStreamEncode(deviceName=specifiedDevice, details=desiredDetails))
                    s.wfile.write(result)
                # end if
                # Otherwise, if the device name is specified.
                elif specifiedDevice != None:
                    # Write all of the current data.
                    s.wfile.write(agent.sampleStreamEncode(deviceName=specifiedDevice))
                # end if device name specified
                # Otherwise, just call a generic current request.
                else:
                    # Write all of the current data.
                    s.wfile.write(agent.sampleStreamEncode())
                # end if
            # end if sample
            # If assets have been requested.
            elif "asset" in s.path:
                # Return an error... because there are no assets.
                s.wfile.write(agent.assetEncode())
            # end if assets
        # end try
        except Exception as ex:
            # If an error occurred, write it.
            error = traceback.format_exc(sys.exc_info()[2])
            s.wfile.write(agent.errorEncode("INVALID_REQUEST", error))
        # end except
        
        # Write the content to the page.
        #s.wfile.write("<html>\n\t<head>\n\t\t<title>MTConnect Agent</title>\n\t</head>")
        #s.wfile.write("\t<body>\n\t\t<p>Just testing web serving.</p>")
        #s.wfile.write("\t\t<p>Page path: "+s.path+"</p></body>\n</html>")
    # end do_GET
# end MTCAgentHandler

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MTCAgentHandler)
    print time.asctime() + "Server starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        agent.isRunning = False
        pass
    
    httpd.server_close()
    #print time.asctime() + "server stops - %s:%s" % (HOST_NAME, PORT_NUMBER)