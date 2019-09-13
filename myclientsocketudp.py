#Author: Animesh Gupta
#Purpose: Python assignment on socket programming (Client code)
#Date:28th Oct
#version: v3.7


import sys
import socket
import time
#import PyPDF2
import re

def create_socket(message,server_name,server_port):
#Define the socket

	client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	print(client_socket)
	
#Send message from Client to Server
	
	client_socket.settimeout(5)

	try:
		print("oooo")
		client_socket.sendto(message.encode(), (server_name, server_port))
		print("Message sent. Waiting for reply.")
		
		response, server_address  = client_socket.recvfrom(150000000)
		# in case of error blocks forever
		print (response)
		print("Got reply back from server! Server reply is:")
			
		
		pattern1 = re.compile(r'\.\w+')
		b = pattern1.findall(message)
		c=b[0]

		pattern2 = re.compile(r'\w+')
		d = pattern2.findall(message)
		e=d[0]
		#print(d[0])

		#print(b[0])

		f= open(e + c,"wb+")
		f.write(response)
		f.close()
		#print(f)
		print (response)
		#print("The name of the file is: ")
		#print(filename.decode())
	
	except:
		print ("Please verify the IP address or port that you have entered. It seems we do not have a Server listening on the specified socket address!")
		#print v
	#print("Message sent. Waiting for reply.")

	
#Receive Server's reply

	#print("Got reply back from server! Server reply is:")
	#print(response.decode())
	#socket.close()
	
if __name__=='__main__':

	#server_name=int(input('Please enter the IPv4 address in the following format - Example: 127.0.0.1'))
	
	
	
	#Code to get an IP as input and (print on screen)
	#print(server_name)
	message=input("Please enter the filename: get \n")
	

	
	server_name = input('Enter destination IP: ')
		
	
	server_port = int(input('Enter the destination port: '))
	create_socket(message,server_name,server_port)
	

	
	
	
