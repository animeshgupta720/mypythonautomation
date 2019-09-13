##Python Restpy script to configure BGP and advertise routes


try:
	import sys
	from ixnetwork_restpy.testplatform.testplatform import TestPlatform
	from IxNetwork import IxNet
	
	#ixNet = IxNet()
	# connect to a windows test platform using the default api server rest port
	
	
	#The script will configure following Ixia chassis 
	ixChassisIpList = ['10.244.9.24']

	# IP - CARD - PORT
	portList = [[ixChassisIpList[0], 2,4], [ixChassisIpList[0], 2, 6]] 
	print(portList)
	
	#Make sure the port below is the port the Ixia API browser is listening on. 

	apiServerIp = '127.0.0.1'
	rest_port=63379
	
	
	#Test the connection with the API browser
	testPlatform = TestPlatform(ip_address='127.0.0.1', rest_port=63379)
	
	
	forceTakePortOwnership = True

	# Console output verbosity: None|request|'request response'
	testPlatform.Trace = 'none'

	#testPlatform.Authenticate(username, password)

	session = testPlatform.Sessions.add() 
	ixNetwork = session.Ixnetwork
	ixNetwork.NewConfig()

	vport1 = ixNetwork.Vport.add(Name='Port1')
	vport2 = ixNetwork.Vport.add(Name='Port2')

	testPorts = [] 
	vportList = [vport.href for vport in ixNetwork.Vport.find()]

	for port in portList:
		print(port[0])
		testPorts.append(dict(Arg1=port[0], Arg2=port[1], Arg3=port[2]))

	ixNetwork.AssignPorts(testPorts,[],vportList,forceTakePortOwnership)


	#Create topology and assign ports 
	ixNetwork.info('Creating Topology Group 1')


	topology1 = ixNetwork.Topology.add(Name='Topo1', Ports=vportList)
	#Create device group
	deviceGroup1 = topology1.DeviceGroup.add(Name='DG1', Multiplier='1')
	ethernet1 = deviceGroup1.Ethernet.add(Name='Eth1')
	ethernet1.Mac.Increment(start_value='00:01:01:01:00:01', step_value='00:00:00:00:00:01')
	#ethernet1.Mac.Increment(start_value='00:01:01:01:00:02', step_value='00:00:00:00:00:01')

	'''ethernet1.EnableVlans.Single(True)'''
    
	#configure Ixia with IPv4

	ixNetwork.info('Configuring IPv4')
	ipv4 = ethernet1.Ipv4.add(Name='Ipv4')
	ipv4.Address.Increment(start_value='1.1.1.1',step_value='0.0.0.1')
	ipv4.Address.Steps.Enabled = True
	ipv4.Address.Steps.Step = '0.0.0.1'

	ipv4.GatewayIp.Decrement(start_value='1.1.1.2', step_value='0.0.0.1')
	ipv4.GatewayIp.Steps.Enabled = True
	ipv4.GatewayIp.Steps.Step = '0.0.0.1'
	#ipv4.GatewayIp.Decrement(start_value='1.1.1.2', step_value='0.0.0.1')


	#Configure OSPF Peering
	ixNetwork.info('Configuring OSPFv2')
	myospf = ipv4.Ospfv2.add(Name='OSPFv2-IF 1')
	myospf.NeighborIp.Decrement(start_value="10.20.0.0", step_value=None)
	myospf.NetworkType.Single("pointtopoint")
	#myospf.NetworkType.Info()
	
	networkGroup1 = deviceGroup1.NetworkGroup.add(Name='OSPF-Routes1', Multiplier='1')
	#Advertise routes via OSPF
	ipv4PrefixPool = networkGroup1.Ipv4PrefixPools.add(NumberOfAddresses='1')
	ipv4PrefixPool.NetworkAddress.Increment(start_value='10.10.0.1', step_value='0.0.0.1')
	ipv4PrefixPool.PrefixLength.Single(32)
	
	#Start all protocols after configuration
	ixNetwork.StartAllProtocols(Arg1='sync')
	
	
	print("\n")
	print("The OSPF configuration for the chassis {} is successful!").format(ixChassisIpList[0])
	
	

except Exception as errMsg:
    print('restPy.Exception:', errMsg)
	
except ImportError:
	print("Looks like the module that you are trying to import is not found")
	
except NameError: 
	print("NameError")
	
except IndentationError:

	print("Indentation 	Error")
	
except SyntaxError:
	print("Exception Error")