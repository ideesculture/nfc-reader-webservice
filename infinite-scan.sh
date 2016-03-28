#!/bin/bash
#!/bin/bash
for (( ; ; ))
do
   now=$(date +"%T")
   python NFCReader2.py --read 7
   #echo "infinite loops [ hit CTRL+C to stop] $now"
done