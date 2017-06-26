#!/usr/bin/python
#
# Finnish Meteorological Institute / Mikko Rauhala (2017)
#
# SmartMet Data Ingestion Module for Vaisala GLD360 Lightning Feed
#
# Universal Ascii Lightning Format (UALF 0)
#
# based on: finpac-salama.py - artok and salama.py - Ville Ilkka
     
import socket
import sys
import time
import os
import json

with open('/smartmet/run/data/vaisala-gld360/cnf/socketreader-config.json') as config_file:
    config = json.load(config_file)

def connect_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((config['host'], config['port']))
        sys.stderr.write("Connected to " 
                         + config['host'] + ":" + str(config['port']) + "\n")
        sys.stderr.write("Output directory: " + config['dir'] + "\n")
        sys.stderr.write("Save interval: " + str(config['saveinterval']) + " min\n")
        return s
    except:
        sys.stderr.write("Connection refused to " 
                         + config['host'] + ":" + str(config['port']) + "\n")
        sys.exit()
     
s = connect_socket()
buffer = ""
output=""
t_end = time.time() + 60 * config['saveinterval']
# reading loop
while True:

    data = s.recv(1024)
    if not data:
        break

    # add the current data read by the socket to a temporary buffer
    buffer += data

    # search complete messages
    messages = buffer.split('\n')

    if time.time() < t_end:
        continue

    # we need at least 2 messages to continue
    if len(messages) == 1:
        continue

    t_end = time.time() + 60 * config['saveinterval']
    # seperator found, iterate across complete messages
    for message in messages [:-1]:
        # handle here the message
        # print repr(message)
        # print message
        # print repr(message.split())
        row = message.split()
        # UALF version 0
        if row[0] == str(0):
            datestr = "%04d%02d%02d" % (int(row[1]), int(row[2]), int(row[3]))
            timestr = "%02d%02d%02d" % (int(row[4]), int(row[5]), int(row[6]))
            lat  = row[8]
            lon  = row[9]
            power = row[10]
            multiplicity = row[11]
            accuracy = row[15]
            output += datestr + timestr + "\t" + lon + "\t" + lat + "\t" + power + "\t" + multiplicity + "\t" + accuracy + "\n"
#            print datestr + timestr + "\t" + lon + "\t" + lat + "\t" + power + "\t" + multiplicity + "\t" + accuracy 
        else:
            print repr(message.split())

    filename = time.strftime('%Y%m%d%H%M%S') + "_vaisala-gld360_lightning.dat"
    with open(config['dir'] + "." + filename, "a") as f:
        print "Writing " + str(len(output.split('\n'))) + " lines to file " + filename
        f.write( output )
        os.rename(config['dir'] + "." + filename, config['dir'] + filename) 
        output = ""

    # set the buffer with the last cutted message
    buffer = messages [-1]

s.close()
