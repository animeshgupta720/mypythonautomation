#!/usr/bin/env python

from netmiko import ConnectHandler
import datetime
import filecmp
import subprocess
#Define dictionary with basic information of network device

ios_r1 = {'device_type': 'cisco_ios',
        'username':'lab',
        'password':'lab123',
        'ip':'198.51.100.3',
        }

#Establish an SSH session

net_connect=ConnectHandler(**ios_r1)

#Send any commands in the enable mode of Cisco ios_r1

output = net_connect.send_command('sh run')
#print(output)

f = open("shrun_latest.txt","w+")
f.write(output)
f.close()
#with open('a','r') as f1:
    #print(f2.read())
#    print(f1.read())


#'''with open("file2.txt","r") as f2:
#       file2=f2.read()
#value = datetime.datetime.now()


if filecmp.cmp("shrun_latest.txt","shrun.txt") is True:
     print("No change in configuration.")
else:
     print("false")

     process1 = subprocess.Popen(['cp',"shrun_latest.txt","shrun.txt"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
     print("Execute the git upload code here")


