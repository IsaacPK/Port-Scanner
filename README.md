# Port-Scanner
Port scanner written in Python

Usage: scanner.py [-h] [--host HOST] [--ports PORTS]

The HOST variable represents the IP address of the host you wish to scan, or a range of hosts separated by a hyphen, or a text file containing a list of IP addresses, one per line. Inputting 192.0.2.10 will scan just that one host, while 192.0.2.10-12 will scan 192.0.2.10, 192.0.2.11, and 192.0.2.12. If the hosts are non-consecutive, or are in different subnets, use a text file containing a list of hosts. Text files must have the .txt suffix.

The PORTS varialbe represnts one port or range of ports to scan, or a text file containing a list of ports. Entering just 80 will scan only port 80, while entering a range delimited by a dash, i.e, 80-1024, will scan all ports from 80 to 1024. If the ports you wish to scan are non-consecutive, instead enter the name of a text file containing a list of ports, one per line. Text files must have the .txt suffix.
