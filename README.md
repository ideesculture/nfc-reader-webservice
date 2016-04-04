# nfc-reader-webservice
NFC reader webservice, bringing NFCReader.py to web app use

## Prerequisites

- python
- pyscard : https://github.com/LudovicRousseau/pyscard

## Installation 

### Mac (tested under El Capitan only)

- install homebrew if not done
- brew install swig git

**important** do not use pip to install pyscard

- git clone https://github.com/LudovicRousseau/pyscard.git
- cd pyscard
- sudo python setup.py build_ext install

**important** the build_ext part is crucial

- add apache user to sudoers with 'sudo visudo' and add the following line :

````
www-data      ALL=(ALL) NOPASSWD:/path/to/nfc-reader-webservice/NFCReader.py
````

### Debian Jessie

````
cd ~ 
apt-get install git swig python-setuptools libpcsclite-dev python-dev
git clone https://github.com/LudovicRousseau/pyscard.git
cd pyscard/
python setup.py build_ext install
````

disable pn533 and nfc driver from the kernel

echo "install nfc /bin/false" >> /etc/modprobe.d/blacklist.conf
echo "install pn533 /bin/false" >> /etc/modprobe.d/blacklist.conf


## Errors and how to solve them

### Crashes

*crashes* are returned through result = crash inside jSON answer

Example :
````
{ "result": "crash", "hint": "smartcard.System python is not installed" }
````

- **smartcard.System python is not installed**
You have not installed pyscard.

- **ImportError: No module named scard**

You may have used "pip install pyscard" or "python setup.py install" for pyscard installation. You have to do a full reinstallation with "sudo python setup.py build_ext install".

- **smartcard.pcsc.PCSCExceptions.EstablishContextException: 'Failure to establish context: Service not available.'**

Drivers for ACR122U NFC Reader are not installed on your computer.

## Copyrights

- Nfc-reader-webservice embeds StevenTso ACS ACR122U NFC Reader / Writer python code. 
https://github.com/StevenTso/ACS-ACR122U-NFC-Reader - MIT License

- all other code : Gautier Michelin (idéesculture), GNU GPL v3, that implies all derivatives go to the same license :-) Please note that this doesn't apply 
to StevenTso ACS ACR122U NFC Reader / Writer python code embedded.
