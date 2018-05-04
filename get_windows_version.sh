#!/bin/bash
#victor.oliveira@gmx.com

#Get Windows version for all computers in a subnet
#Programs needed:
#nmap
#net (from samba)

SUBNET=196.1.1.0/24
USER=
PASSWORD=

HOSTS=$(nmap $SUBNET --open -p 135,445 -Pn -n| grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
for HOST in $HOSTS; do
	HOSTNAME=$(net rpc info -U "$USER"%"$PASSWORD" -I "$HOST"| grep "Domain Name"| cut -d\  -f3)
	WINVER=$(net rpc registry getvalue "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" ProductName -U "$USER"%"$PASSWORD" -I "$HOST"| grep -Eo '".*"')
	echo "$HOST":"$HOSTNAME":"$WINVER"
done
