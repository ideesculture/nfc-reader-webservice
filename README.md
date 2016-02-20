# nfc-reader-webservice
NFC reader webservice, bringing NFCReader.py to web app use

## Prerequisites

- python
- pyscard : https://github.com/LudovicRousseau/pyscard

## Errors and how to solve them

### Crashes

*crashes* are returned through result = crash inside jSON answer

Example :
````
{ "result": "crash", "hint": "smartcard.System python is not installed" }
````

- **smartcard.System python is not installed**
pyscard - python for smart cards

## Copyrights

- Nfc-reader-webservice embeds StevenTso ACS ACR122U NFC Reader / Writer python code. 
https://github.com/StevenTso/ACS-ACR122U-NFC-Reader - MIT License

- all other code : Gautier Michelin (idéesculture), GNU GPL v3, that implies all derivatives go to the same license :-) Please note that this doesn't apply 
to StevenTso ACS ACR122U NFC Reader / Writer python code embedded.
