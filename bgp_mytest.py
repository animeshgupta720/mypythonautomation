#Python Restpy script to configure BGP and advertise routes

try:
	import sys
	from ixnetwork_restpy.testplatform.testplatform import TestPlatform
	#from IxNetwork import IxNet
	from ixnetwork_restpy.assistants.statistics.statviewassistant import StatViewAssistant

	import time

	#The script will configure following Ixia chassis 
	ixChassisIpList = ['10.244.9.24']

	# IP - CARD - PORT
	portList = [[ixChassisIpList[0], 2,4], [ixChassisIpList[0], 2, 6]] 
	print(portList)
	
	#Make sure the port below is the port the Ixia API browser is listening on. 
	
	apiServerIp = '127.0.0.1'
	rest_port=11009

	#try: 
	testPlatform = TestPlatform(ip_address='127.0.0.1', rest_port=11009)
	forceTakePortOwnership = True

	# Console output verbosity: None|request|'request response'
	#testPlatform.Trace = 'request_response'
	testPlatform.Trace = 'none'

	#testPlatform.Authenticate(username, password)
	#Access the session you created based on the conection information provided above. For a different connection info, a different session will be created.

	session = testPlatform.Sessions.add()
	ixNetwork = session.Ixnetwork
	
	#Clear any configuration that may be present
	ixNetwork.NewConfig()

	vport1 = ixNetwork.Vport.add(Name='Port1')
	vport2 = ixNetwork.Vport.add(Name='Port2')

	testPorts = [] 
	vportList = [vport.href for vport in ixNetwork.Vport.find()]
	#vport1 = ixNetwork.Vport.find()[0]
	#vport2 = ixNetwork.Vport.find()[1]
	print("**************")
	print(vportList)
	for port in portList:
		print(port[0])
		testPorts.append(dict(Arg1=port[0], Arg2=port[1], Arg3=port[2]))

	ixNetwork.AssignPorts(testPorts,[],vportList,forceTakePortOwnership)
	mytopologystatus = ixNetwork.GetTopologyStatus()
	for element in mytopologystatus:
		print(element)
	#Create topology and assign ports 
	ixNetwork.info('Creating Topology Group 1')

	
	topology1 = ixNetwork.Topology.add(Name='Topo1', Ports=vportList)
	print("This is tpology content")
	print(topology1.Vports[0])
	deviceGroup1 = topology1.DeviceGroup.add(Name='DG1', Multiplier='1') 
	ethernet1 = deviceGroup1.Ethernet.add(Name='Eth1')
	ethernet1.Mac.Increment(start_value='00:01:01:01:00:01', step_value='00:00:00:00:00:01')
	#ethernet1.Mac.Increment(start_value='00:01:01:01:00:02', step_value='00:00:00:00:00:01')

	

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
	#Here
	ixNetwork.info('Configuring BgpIpv4Peer 1')
	bgp1 = ipv4.BgpIpv4Peer.add(Name='Bgp1')
	bgp1.DutIp.Decrement(start_value='1.1.1.2', step_value='0.0.0.0')
	bgp1.DutIp.Steps.Enabled = True
	bgp1.DutIp.Steps.Step = '0.0.0.1'
	bgp1.Type.Single('internal')
	bgp1.LocalAs2Bytes.Increment(start_value=101, step_value=0)

	
	print("Advertise routes via BGP")
	networkGroup1 = deviceGroup1.NetworkGroup.add(Name='BGP-Routes1', Multiplier='1')
	ipv4PrefixPool = networkGroup1.Ipv4PrefixPools.add(NumberOfAddresses='10')
	ipv4PrefixPool.NetworkAddress.Increment(start_value='10.10.0.1', step_value='0.0.0.1')
	ipv4PrefixPool.PrefixLength.Single(32)
	

	print("Creating traffic item")
	traffic_item1 = ixNetwork.Traffic.TrafficItem.add(Name='My IPv4 Traffic Item1', TrafficType='ipv4', TrafficItemType='l2L3', Enabled=True,BiDirectional=True)
	
	#traffic_item2 = ixNetwork.Traffic.TrafficItem.add(Name='My IPv4 Traffic Item2', TrafficType='ipv4', TrafficItemType='l2L3', Enabled=True, BiDirectional=True)
	
	print("Creating EndpointSet")
	
	
	scaleDest = [
		{
			'arg1': ipv4.href,
			'arg2': 2,
			'arg3': 1,
			'arg4': 1,
			'arg5': 1
		}
	]
	print("This is ipv4.href")
	print(ipv4.href)
	ixNetwork.info(scaleDest)
	endpoint_set1 = traffic_item1.EndpointSet.add(Sources=topology1, ScalableDestinations=scaleDest)
	
	traffic_item1.Tracking.find()[0].TrackBy = ['trackingenabled0']
	flowgroup1 = traffic_item1.Tracking.find()[0]
	#print(flowgroup1)
	#tracking = traffic_item1.Tracking.find(TrackBy="trafficitems")
	#testPlatform.info(tracking.TrackBy)

	#endpoint_set2 = traffic_item2.EndpointSet.add(ScalableSources=scaleDest, Destinations=topology1)
	ixNetwork.StartAllProtocols(Arg1='sync')
	time.sleep(30)
	
	ixNetwork.info('Verify protocol sessions\n')
	protocolsSummary = StatViewAssistant(ixNetwork, 'Protocols Summary')
	protocolsSummary.CheckCondition('Sessions Not Started', StatViewAssistant.EQUAL, 0)
	protocolsSummary.CheckCondition('Sessions Down', StatViewAssistant.EQUAL, 0)
	ixNetwork.info(protocolsSummary)
	traffic_item1.Generate()
	#ixNetwork.Traffic.TrafficItem.find().Generate()
	time.sleep(20)
	ixNetwork.Traffic.Apply()
	time.sleep(20)
	ixNetwork.Traffic.Start()
	time.sleep(10)
	trafficItemStatistics = StatViewAssistant(ixNetwork, 'Traffic Item Statistics')
	ixNetwork.info('{}\n'.format(trafficItemStatistics))
	
	txFrames = trafficItemStatistics.Rows[0]['Tx Frames']
	rxFrames = trafficItemStatistics.Rows[0]['Rx Frames']
	ixNetwork.info('\nTraffic Item Stats:\n\tTxFrames: {}  RxFrames: {}\n'.format(txFrames, rxFrames))
	

	'''#ixNetwork.commit()
	print("Traffic Apply and Start")
	
	
	#
	#time.sleep(10)
	#ixNetwork.Traffic.Start()
	#ixNetwork.StopAllProtocols(Arg1='sync')
	print("\n")
	print("The BGP configuration for the chassis {} is successful!").format(ixChassisIpList[0])
	#flowStatistics = StatViewAssistant(ixNetwork, 'Flow Statistics')
	#ixNetwork.info('{}\n'.format(flowStatistics))'''
	
	
	
	'''for rowNumber,flowStat in enumerate(flowStatistics.Rows):
		ixNetwork.info('\n\nSTATS: {}\n\n'.format(flowStat))
		ixNetwork.info('\nRow:{}  TxPort:{}  RxPort:{}  TxFrames:{}  RxFrames:{}\n'.format(rowNumber, flowStat['Tx Port'], flowStat['Rx Port'],flowStat['Tx Frames'], flowStat['Rx Frames']))
			
	flowStatistics = StatViewAssistant(ixNetwork, 'Traffic Item Statistics')
	ixNetwork.info('{}\n'.format(flowStatistics))'''


except Exception as errMsg:
    print('restPy.Exception:', errMsg)


	





