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


### Debian Jessie, Ubuntu 16.04

Install all the prerequisites through apt-get, you will need to be root at this step.
For some of the next steps too, please check with/without being root if you are stuck somewhere.

````
apt-get install git swig python-setuptools libpcsclite-dev python-dev gcc pcscd
````

You will need pyscard. As the version is easier from LudovicRousseau github repo, I recommend it to you.

````
cd ~ 
git clone https://github.com/LudovicRousseau/pyscard.git
cd pyscard/
python setup.py build_ext install
````

disable pn533 and nfc driver from the kernel

````
echo "install nfc /bin/false" >> /etc/modprobe.d/blacklist.conf
echo "install pn533 /bin/false" >> /etc/modprobe.d/blacklist.conf
````

**important** : reboot at this step, as we will need to start pcscd and it needs to have those modules disables

launch pcscd if it is not already started

````
pcscd &
````

install nfc-reader-webservice

````
mkdir -p /opt
cd /opt
git clone https://github.com/ideesculture/nfc-reader-webservice.git
````

test (command line)

````
cd /opt/nfc-reader-webservice
python NFCReader.py --read 8
````

run (python server) on port 81

````
cd /opt/nfc-reader-webservice
python NFCReader_webservice.py 81
````

test (browser) : go to http://localhost:81

**recommended** : create a local dns name you can use inside your code and affect to each computer that will have a NFC reader

````
nano /etc/hosts
````

go to the end file, and type in those lines

````
127.0.0.1 nfc-reader-webservice.dev
````

and save.


Now you can use http://nfc-reader-webservice.dev:81/?line=1 (with line as the number of a 4 bytes line you want to read on the NFC chip).

````
curl http://nfc-reader-webservice.dev:81/?line=1
````

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
