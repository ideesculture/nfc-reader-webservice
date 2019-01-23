#!/bin/bash
# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import messagebox

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


def readTagObjectWindow():
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
        messagebox.showinfo('NFC', 'erreur')
    else:
        messagebox.showinfo('NFC', "La puce contient l'objet "+str(result))

def readTagPlayerWindow():
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
        messagebox.showinfo('NFC', 'erreur')
    else:
        messagebox.showinfo('NFC', "La puce contient le joueur "+str(result))

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

Mafenetre.title('Lecture/écriture badges Zoodéfis')
#Mafenetre.geometry('700x100+200+200')
Mafenetre.rowconfigure(0, weight=1)
Mafenetre.columnconfigure(0, weight=1)

# Création d'un widget Button (bouton Lancer)
BoutonLancer = Button(Mafenetre, text ='Lire la puce objet', command = readTagObjectWindow)
# Positionnement du widget avec la méthode pack()
#BoutonLancer.pack(side = LEFT, padx = 5, pady = 2)
BoutonLancer.grid(row=0, column=0, sticky="nsew")

# Création d'un widget Button (bouton Lancer)
BoutonLancerJoueur = Button(Mafenetre, text ='Lire la puce joueur', command = readTagPlayerWindow)
# Positionnement du widget avec la méthode pack()
#BoutonLancerJoueur.pack(side = LEFT, padx = 5, pady = 2)
BoutonLancerJoueur.grid(row=1, column=0, sticky="nsew")

txt = Entry(Mafenetre,width=10)
#txt.pack(side = LEFT, padx = 0, pady = 10)
txt.grid(row=2, column=0, sticky="nsew")

def writeTagObjectWindow():
    value = str(txt.get());
    writeTag(7, value);
    messagebox.showinfo('NFC', "L'objet : "+value+" a été écrit")
    #break

def writeTagPlayerWindow():
    value = str(txt.get());
    writeTag(8, value);
    messagebox.showinfo('NFC', "Le joueur : "+value+" a été écrit")
    #break

BoutonEcrire = Button(Mafenetre, text ='Ecrire la puce objet', command = writeTagObjectWindow)
# Positionnement du widget avec la méthode pack()
#BoutonEcrire.pack(side = LEFT, padx = 5, pady = 2)
BoutonEcrire.grid(row=3, column=0, sticky="nsew")

BoutonEcrireJoueur = Button(Mafenetre, text ='Ecrire la puce joueur', command = writeTagPlayerWindow)
# Positionnement du widget avec la méthode pack()
#BoutonEcrireJoueur.pack(side = LEFT, padx = 5, pady = 2)
BoutonEcrireJoueur.grid(row=4, column=0, sticky="nsew")

# Création d'un widget Button (bouton Quitter)
BoutonQuitter = Button(Mafenetre, text ='Quitter', command = Mafenetre.destroy)
#BoutonQuitter.pack(side = RIGHT, padx = 5, pady = 10)
BoutonQuitter.grid(row=6, column=0, sticky="nsew")

Texte = StringVar()
#readTagWindow()

Mafenetre.mainloop()




