#Thsi script will load a topolgy from IxNetwork application and initiate traffic from port 2-4 and then capture the the traffic from port 2-6.
#After capturing the traffic in a wireshark file, this script will parse through the capture file using Scapy module to check cos value == 5 in each received packet.


from ixnetwork_restpy.testplatform.testplatform import TestPlatform
from ixnetwork_restpy.files import Files
import time
from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant
from scapy.all import *


#The following function receives the values from a Flask run GUI on which user enters these values manually.

def ixia_qos(result,packetcount,option):
# connect to a test platform, create a session and get the root IxNetwork object
	test_platform = TestPlatform('127.0.0.1', rest_port=63061)
	forceTakePortOwnership = True
	test_platform.Trace = 'none'
	sessions = test_platform.Sessions.add()
	ixChassisIpList = ['10.244.9.24']
	ixnetwork = sessions.Ixnetwork
	#test_platform.Trace = 'request_response'
	ixnetwork.NewConfig()

	#create the logical ports for Ixia

	vport1 = ixnetwork.Vport.add(Name='Port1')
	vport2 = ixnetwork.Vport.add(Name='Port2')


	vportList = [vport.href for vport in ixnetwork.Vport.find()]

	portList = [[ixChassisIpList[0], 2,4]]




	#### load the saved IxNetwork configuration
	ixnetwork.LoadConfig(Files(result,local_file=True))
	testPorts = []
	for port in portList:
			print("Chassis IP address is {}".format(port[0]))
			testPorts.append(dict(Arg1=port[0], Arg2=port[1], Arg3=port[2]))

	forceTakePortOwnership=True


	#Assign the ports to the configuration

	ixnetwork.AssignPorts(testPorts,[],vportList,forceTakePortOwnership)


	#Start all protocols

	print("*******************Starting Protocols************************")

	ixnetwork.StartAllProtocols(Arg1='sync')
	time.sleep(20)


	print("*******************Creating Traffic Items************************")

	#Define traffic items with specific trafic types.
	traffic_item1 = ixnetwork.Traffic.TrafficItem.find(TrafficType='ipv4')
	traffic_item2 = ixnetwork.Traffic.TrafficItem.find(TrafficType='ipv6')

	print(traffic_item1)
	#print(traffic_item2)

	### Define the framecount that you want to send through the Ixia port. 

	

	print("*******************Define the number of packets you want to send************************")

	configElement = traffic_item1.ConfigElement.find()
	transmissioncontrol = configElement.TransmissionControl
	transmissioncontrol.update(FrameCount=packetcount)
	test_platform.info(transmissioncontrol.FrameCount)
	#print(configElement)


	#print("Choose the type of traffic you want to send:")

	print("\n")

	#a = int(input("Enter 1. IPv4 or 2. IPv6 or 3. Both: "))


	i=0

	###Run the traffic IPv4 traffic if the user enters 1 as an option.

	if option == 1:
		
		
		#####Only enable IPv4 traffic as defined in the test case.
		
		#traffic_item1.update(Enabled=True)
		traffic_item1.find()[1].update(Enabled=False)
		traffic_item1.find()[3].update(Enabled=False)

		time.sleep(5)
		traffic_item1.Generate()
		time.sleep(5)
		ixnetwork.Traffic.Apply()
		time.sleep(5)

		ixnetwork.StartCapture()
		time.sleep(5)
		ixnetwork.Traffic.Start()
		time.sleep(10)

		ixnetwork.StopCapture()
		ixnetwork.SaveCapture("C:\Python27\Programs",'_QoS')


		pcapFile = "EGRESS - NETWORK TRUNK_HW_QoS.cap"
		#####Parse through the Wireshark file to check each packet for a COS value ==5. Print a statement if the value is not equal to 5"
		for packet in rdpcap(pcapFile):
			#ixnetwork.info('\nPacket: {}:\n'.format(index))
			#print("here")
			try:
				dot1q = packet['Dot1Q']
			#priority = dot1q[prio]
				if (packet.prio)==5:
					print("cos == 5")
					i=i+1
					continue
				else:
					print("Packet does not have priorty set to 5")
			except:
				pass
		print("Total IPv4 packets checked {}".format(i))
		#	time.sleep(10)
		#ixnetwork.Traffic.Stop()


	###Run the traffic IPv6 traffic if the user enters 2 as an option.

	elif option == 2:
		
		
		#####Only enable IPv6 traffic as defined in the test case.

		#traffic_item1.update(Enabled=True)
		traffic_item1.find()[0].update(Enabled=False)
		traffic_item1.find()[2].update(Enabled=False)


		print(configElement)
		time.sleep(5)
		traffic_item1.Generate()
		time.sleep(5)
		ixnetwork.Traffic.Apply()
		time.sleep(5)

		ixnetwork.StartCapture()
		time.sleep(5)
		ixnetwork.Traffic.Start()
		time.sleep(10)

		ixnetwork.StopCapture()
		ixnetwork.SaveCapture("C:\Python27\Programs",'_QoS')


		pcapFile = "EGRESS - NETWORK TRUNK_HW_QoS.cap"
		####Parse through the Wireshark file to check each packet for a COS value ==5. Print a statement if the value is not equal to 5"
		for packet in rdpcap(pcapFile):
			#ixnetwork.info('\nPacket: {}:\n'.format(index))
			#print("here")
			try:
				dot1q = packet['Dot1Q']
			#priority = dot1q[prio]
				if (packet.prio)==5:
					print("cos == 5")
					i=i+1
					continue
				else:
					print("Packet does not have priorty set to 5")
			except:
				pass
		print("Total IPv6 packets checked {}".format(i))

		#	time.sleep(10)
		#ixnetwork.Traffic.Stop()
		
	else:

		time.sleep(5)
		traffic_item1.Generate()
		time.sleep(5)
		ixnetwork.Traffic.Apply()
		time.sleep(5)

		ixnetwork.StartCapture()
		time.sleep(5)
		ixnetwork.Traffic.Start()
		time.sleep(10)


		ixnetwork.StopCapture()
		ixnetwork.SaveCapture("C:\Python27\Programs",'cap')


		pcapFile = "EGRESS - NETWORK TRUNK_HWcap.cap"
		
		#####Parse through the Wireshark file to check each packet for a COS value ==5. Print a statement if the value is not equal to 5"
		for packet in rdpcap(pcapFile):
			#ixnetwork.info('\nPacket: {}:\n'.format(index))
			#print("here")
			try:
				dot1q = packet['Dot1Q']
			#priority = dot1q[prio]
				if (packet.prio)==5:
					print("cos == 5")
					i=i+1
					continue
				else:
					print("Packet does not have priorty set to 5")
			except:
				pass
		print("Total IPv4 & IPv6 packets checked {}".format(i))
		#	time.sleep(10)
		#ixnetwork.Traffic.Stop()