#!/bin/bash
# -*- coding: UTF-8 -*-
from tkinter import *
import random
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import SocketServer
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


def readTagWindow():
	result = readTag(7)
	if (result is None):
		result = readTag(7)
	if (result is None):
		result = readTag(7)
	if (result is None):
		result = readTag(7)
	if (result is None):
		result = readTag(7)
	if (result is None):
		result = readTag(7)
	if (result is None):
		Texte.set('Erreur de lecture')
	else:
		nb = random.randint(1,6)
		Texte.set('Résultat -> ' + str(result))


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
    #try:
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
    #except Exception,e: print str(e)

def writeTag(page, value):
    if type(value) != str:
        return "Value input should be a string"
        exit()
    while(1):
        if len(value) == 8:
            #try:
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
            #except Exception, e:
                #continue
        else:
            return "Must have a full 4 byte write value"
            break

# Création de la fenêtre principale (main window)
Mafenetre = Tk()

Mafenetre.title('Dé à 6 faces')
Mafenetre.geometry('300x100+400+400')

# Création d'un widget Button (bouton Lancer)
BoutonLancer = Button(Mafenetre, text ='Actualiser', command = readTagWindow)
# Positionnement du widget avec la méthode pack()
BoutonLancer.pack(side = LEFT, padx = 5, pady = 2)

# Création d'un widget Button (bouton Quitter)
BoutonQuitter = Button(Mafenetre, text ='Quitter', command = Mafenetre.destroy)
BoutonQuitter.pack(side = RIGHT, padx = 5, pady = 10)

Texte = StringVar()
readTagWindow()

# Création d'un widget Label (texte 'Résultat -> x')
LabelResultat = Label(Mafenetre, textvariable = Texte, fg ='red', bg ='white')
LabelResultat.pack(side = LEFT, padx = 5, pady = 5)

Mafenetre.mainloop()




