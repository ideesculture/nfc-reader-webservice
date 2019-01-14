#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import re, argparse
from smartcard.System import readers
import datetime, sys
import json

#ACS ACR122U NFC Reader
#Suprisingly, to get data from the tag, it is a handshake protocol
#You send it a command to get data back
#This command below is based on the "API Driver Manual of ACR122U NFC Contactless Smart Card Reader"
COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00] #handshake cmd needed to initiate data transfer

# Disable the standard buzzer when a tag is detected, Source : https://gist.github.com/nixme/2717287
DISABLEBEEP = [0xFF, 0x00, 0x52, 0x00, 0x00]

# get all the available readers
r = readers()
reader = r[0]
result = ""

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        #self.wfile.write("<html><body><h1>hi!</h1></body></html>")
        result = readTag(8)
        if (result is None):
            result = readTag(8)
        if (result is None):
            result = readTag(8)
        if (result is None):
            result = readTag(8)
        if (result is None):
            result = readTag(8)
        if (result is None):
            result = readTag(8)
        if (result is None):
            self.wfile.write(json.dumps({"usingreader": 0, "result":"error", "value":result}, indent=4, separators=(',', ': ')));
        else :
            self.wfile.write(json.dumps({"usingreader": 0, "result":"success", "value":result}, indent=4, separators=(',', ': ')));

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

def stringParser(dataCurr):
#--------------String Parser--------------#
    #([85, 203, 230, 191], 144, 0) -> [85, 203, 230, 191]
    if isinstance(dataCurr, tuple):
        temp = dataCurr[0]
        code = dataCurr[1]
    #[85, 203, 230, 191] -> [85, 203, 230, 191]
    else:
        temp = dataCurr
        code = 0

    dataCurr = ''

    #[85, 203, 230, 191] -> bfe6cb55 (int to hex reversed)
    for val in temp:
        # dataCurr += (hex(int(val))).lstrip('0x') # += bf
        dataCurr += format(val, '#04x')[2:] # += bf

    #bfe6cb55 -> BFE6CB55
    dataCurr = dataCurr.upper()

    #if return is successful
    if (code == 144):
        return dataCurr

def readTag(page):
    try:
        connection = reader.createConnection()
        status_connection = connection.connect()
        connection.transmit(DISABLEBEEP)
        connection.transmit(COMMAND)
        #Read command [FF, B0, 00, page, #bytes]
        resp = connection.transmit([0xFF, 0xB0, 0x00, int(page), 0x04])
        dataCurr = stringParser(resp)

        #only allows new tags to be worked so no duplicates
        if(dataCurr is not None):
            return dataCurr
        else:
            return "Something went wrong. Page " + str(page)
    except Exception,e: print str(e)

def writeTag(page, value):
    if type(value) != str:
        return "Value input should be a string"
        exit()
    while(1):
        if len(value) == 8:
            try:
                connection = reader.createConnection()
                status_connection = connection.connect()
                connection.transmit(DISABLEBEEP)
                connection.transmit(COMMAND)
                WRITE_COMMAND = [0xFF, 0xD6, 0x00, int(page), 0x04, int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), int(value[6:8], 16)]
                # Let's write a page Page 9 is usually 00000000
                resp = connection.transmit(WRITE_COMMAND)
                if resp[1] == 144:
                    return "Wrote " + value + " to page " + str(page)
                    break
            except Exception, e:
                continue
        else:
            return "Must have a full 4 byte write value"
            break

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()