#Name: Animesh Gupta
#!/usr/bin/env python


from flask import Flask,render_template, Markup, request
import json
from napalm import get_network_driver
import time
import threading
import datetime
from netmiko import ConnectHandler

#from validateIPfunction import validipcheck

app = Flask(__name__)



@app.route("/test",methods=['GET','POST'])
def myOSPFconfig():
	return render_template("ospfconfigixia.html")


@app.route('/R1')

def form_page_r1():
    return render_template('ixia_wftemplate.html')


@app.route('/myR1config',methods=['GET','POST'])

def myPage_r1():
    print("here")
    value_ip = request.form['myVar']
    value_as = request.form['myVar2']
    
    value_neighbor = request.form['myVar3']
    value_remoteas = request.form['myVar4']
    #myLoopback = request.form['myVar5']


    #return ("The configuration has been modified successfully!")
    




    ios_r1 = {'device_type':'cisco_ios',
		'username':'lab',
		'password':'lab123',
		'ip':'198.51.100.3'}

    net_connect = ConnectHandler(**ios_r1)
	#value_ip = '10.10.10.1'
	#value_as = '65305'
	#value_neighbor = '10.10.10.2'
	#value_remoteas = '65305'
    commands_r1 = ['int f0/1','ip add {} 255.255.255.0'.format(value_ip),'no shut','router bgp {}'.format(value_as),
        'neighbor {} remote-as {}'.format(value_neighbor,value_remoteas)]
    output_r1 = net_connect.send_config_set(commands_r1)
    print(output_r1)


    ios_r2 = {'device_type':'cisco_ios',
		'username':'lab',
		'password':'lab123',
		'ip':'198.51.100.4'}

    net_connect = ConnectHandler(**ios_r2)
    value_ip = '10.10.10.2'
    value_as = '65305'
    value_neighbor = '10.10.10.1'
    value_remoteas = '65305'
    commands_r2 = ['int f0/1','ip add {} 255.255.255.0'.format(value_ip),'no shut','router bgp {}'.format(value_as),
        'neighbor {} remote-as {}'.format(value_neighbor,value_remoteas)]
    output_r2 = net_connect.send_config_set(commands_r2)
    return "Testing cmpleted successfully between Ixia and IOS-XR and the test results have been saved!!!"

               
    #bodyText = Markup("The input from the form is {}".format(myUsername))
    #return render_template('mytemplate.html',bodyText=bodyText)    

if __name__ == "__main__":

	app.run(debug=True, host='127.0.0.1',port=8080)
	
