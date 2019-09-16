# network-test-automation

This project contains the automation scripts to automate network device testing. For example, this project contains a Flask script that 
creates a webserver using HTML templates containing fields to receive network configuration parameters which are taken as an input 
from user and fed into the network automation script in the backend. The network automation script will take these user input values 
from GUI and configure a Cisco router, load an IxNetwork topology and then run tests between them by sending traffic. 

In the qostest.py script, we are testing whether all the packets sent by Ixia have been tgged a cos value = 5 by the Cisco router.
