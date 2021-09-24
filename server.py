#  coding: utf-8 
import socketserver
from urllib.parse import urlparse
from mimetypes import guess_type
import os
import time
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright 漏 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        data_decode = self.data.decode('utf-8')
        data_first_line = data_decode.split("\r\n")[0]
        #print(data_first_line.split())
        method, url, version = data_first_line.split()
        parsed_url = urlparse(url)
        path = "www" + parsed_url.path
        if(path[-1] == '/'):
            path = path + 'index.html'
        else:
            #print(path)
            content_type = guess_type(path)[0]
            if(content_type == None):
                if(os.path.exists(path + '/')):
                    date = time.strftime("DATE: %a, %d %b %Y %I:%M:%S %p %Z\r\n", time.gmtime()) + "\r\n"
                    header = "%s %s %s"%(version, "301", "Moved Permanently") + "\r\n"
                    connection = "Connection: close"+ "\r\n\r\n"
                    message = header + date + connection + parsed_url.path + '/' 
                    
                    #print(message)
                    self.request.sendall(bytearray(message,'utf-8'))
                    self.request.close()
                    return
                else:
                    header = "%s %s %s"%(version, "404", "NOT Found") + "\r\n"
                    date = time.strftime("DATE: %a, %d %b %Y %I:%M:%S %p %Z\r\n", time.gmtime()) + "\r\n"
                    connection = "Connection: close"+ "\r\n\r\n"
                    message = header + date + connection 
                    #print(message)
                    self.request.sendall(bytearray(message,'utf-8'))
                    self.request.close()
                    return  
        if(method == 'GET'):      
            try:
                f =  open(path, "r")
                    
            except Exception as e:
                header = "%s %s %s"%(version, "404", "NOT Found") + "\r\n"
                date = time.strftime("DATE: %a, %d %b %Y %I:%M:%S %p %Z\r\n", time.gmtime()) + "\r\n"
                connection = "Connection: close"+ "\r\n\r\n"
                message = header + date + connection 
                #print(message)
                self.request.sendall(bytearray(message,'utf-8'))
                self.request.close()
                return
            content = f.read()        
            header = "%s %s %s"%(version, "200", "OK") + "\r\n"
            content_type_m = "Content-Type: %s; charset=%s"%(guess_type(path)[0], 'utf-8') + "\r\n"
            #print(path)
            date = time.strftime("DATE: %a, %d %b %Y %I:%M:%S %p %Z\r\n", time.gmtime()) + "\r\n"
            content_length = "Content-Length: %s"%( str(len(content)))+ "\r\n" 
            connection = "Connection: close"+ "\r\n\r\n"
            message = header + content_type_m + content_length + date + connection  + content
            #print(message)
            self.request.sendall(bytearray(message,'utf-8')) 
            f.close() 
              
        else:
            header = "%s %s %s"%(version, "405", "405 Method Not Allowed") + "\r\n"
            date = time.strftime("DATE: %a, %d %b %Y %I:%M:%S %p %Z\r\n", time.gmtime()) + "\r\n"
            connection = "Connection: close"+ "\r\n\r\n"
            message = header + date + connection 
            #print(message)
            self.request.sendall(bytearray(message,'utf-8'))
        self.request.close()
        return

        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    #socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    #Test = "good/nice/hh/"
    #print(guess_type(Test))
    
