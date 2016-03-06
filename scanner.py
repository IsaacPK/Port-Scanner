import socket
from datetime import datetime
import argparse
import sys
from string import rfind

# To do: implement protocols other than TCP, do traceroute?, HTML output of results

# Scans a set of ports on the IP address given by 'ip'
def scan(ip, portStart, portEnd, portList):
	serverIP  = socket.gethostbyname(ip)
	
	# Prints info about which host and ports we are about to scan
	print "*" * 60
	if(len(portList) > 0):
		print "Scanning ports in file", ports, "for remote host", serverIP
	elif(portStart == portEnd):
		print "Scanning remote host", serverIP, "on port", portStart
	else:
		print "Scanning remote host", serverIP, "on ports", portStart, "through", portEnd
	print "*" * 60
	
	# Check what time the scan started
	t1 = datetime.now()
	
	# Ports are specified by portStart and portEnd, unless portList has length > 0.
	# In that case ports are specified by the portList generated from a file.
	# The program will exit if it encounters an error here.
	try:
		if(len(portList) > 0):
			for port in portList:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				res = sock.connect_ex((serverIP, port))
				if res == 0:
					print "Port {}: \t Open".format(port)
				sock.close()
		else:
			for port in range(portStart,portEnd + 1):  
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				res = sock.connect_ex((serverIP, port))
				#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
				#sock.sendto(MESSAGE, (serverIP, port))
				if res == 0:
					print "Port {}: \t Open".format(port)
				sock.close()

	except KeyboardInterrupt:
		print "Ctrl+C signal received"
		sys.exit()

	except socket.gaierror:
		print "Could not resolve hostname. Exiting."
		sys.exit()

	except socket.error:
		print "Couldn't connect to server. Exiting."
		sys.exit()
	
	# Check the time again
	t2 = datetime.now()
	
	# Calculate how long the port scanning took
	total =  t2 - t1
	
	# Print the results
	print 'Scanning Completed in: ', total


# Parse command line arguments
parser = argparse.ArgumentParser(description='Process host and ports')
parser.add_argument('--host', '-o', help='IP address of the host you wish to scan, or a range of hosts separated by a hyphen. For example, 192.0.2.10-12 will scan 192.0.2.10, 192.0.2.11, and 192.0.2.12. If the hosts are non-consecutive, or are in different subnets, instead enter the name of a text file containing a list of hosts. Text files must have the .txt suffix.', type=str)
parser.add_argument('--ports', '-p', help='A port or range of ports to scan. Enter the beginning and end of the range separated by a hyphen, i.e., 80-1024. If the ports are non-consecutive, instead enter the name of a text file containing a list of ports. Text files must have the .txt suffix.', type=str)
args = parser.parse_args()

serverIPs = args.host
ports = args.ports
pStart, pEnd = -1, -1

# Determine whether to read the list of ports from a text file, or whether
# to process a range of ports or a single port from the command line
portList = []
if(ports.find('.txt') > 0):
	pList = list(open(ports))
	for port in pList:
		portList.append(int(port.strip()))
elif(ports.find('-') >= 0):
	pStart, pEnd = ports.split('-')
	pStart = int(pStart)
	pEnd = int(pEnd)
	if(pStart > pEnd):
		print "Invalid port range."
		sys.exit()
else:
	pStart, pEnd = int(ports), int(ports)

# Determine whether to read a list of hosts from file or from the command
# line. Parses either a range of ports or a single port.
hostList = []
if(serverIPs.find('.txt') > 0):
	hostList = list(open(serverIPs))
	for host in hostList:
		scan(host.strip(), pStart, pEnd, portList)
		print '\n'
elif(serverIPs.find('-') >= 0):
	base, end = serverIPs.split('-')
	dotLocation = base.rfind('.')
	start = base[dotLocation + 1:len(base)]
	base = base[0:dotLocation + 1]
	start = int(start)
	end = int(end)
	if(start > end):
		print "Invalid host range."
		sys.exit()
	
	for hostEnd in range(start, end + 1):
		scan(base + str(hostEnd), pStart, pEnd, portList)
		print '\n'
else:
	scan(serverIPs, pStart, pEnd, portList)
