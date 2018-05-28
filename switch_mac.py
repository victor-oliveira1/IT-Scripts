#!/bin/python3
#Get MAC addresses via telnet from managed switches

#Copyright © 2018 Victor Oliveira <victor.oliveira@gmx.com>
#This work is free. You can redistribute it and/or modify it under the
#terms of the Do What The Fuck You Want To Public License, Version 2,
#as published by Sam Hocevar. See the COPYING file for more details.

import telnetlib
import sys
import re
import macvendor

user = 'USER'
password = 'PASSWORD'
host = sys.argv[1]
port = 23
timeout = 5

def Send(data=None):
    if data:
        data += '\n'
    else:
        data = '\n'
    data_encoded = data.encode()
    tn.write(data_encoded)
    
def Read(data):
    data_encoded = data.encode()
    out_encoded = tn.read_until(data_encoded, timeout)
    out_decoded = out_encoded.decode()
    return out_decoded

tn = telnetlib.Telnet(host, port)
Read('Username:')
Send(user)
Read('Password:')
Send(password)
Send('system-view')
Send('display mac-address')
Read('(s)\r\n')

maclist = str()
tmp = Read('---- More ----')
while True:
    if 'More' in tmp:
        maclist += tmp
        Send()
        tmp = Read('---- More ----')
    else:
        break

print('Writing file...')
with open(host + '.csv', 'w') as file:
    file.write('"PORT";"VLAN";"MAC";"VENDOR";"MACS ON PORT"\n')
    for line in maclist.split('\r\n'):
        try:
            #Removing weird strings
            line = re.findall('\w{4}-\w{4}-\w{4}.*', line)[0].split()

            mac = line[0]
            vlan = line[1]
            port = line[3]
            vendor = macvendor.Vendor(mac)[1]
            macs_on_port = maclist.count(port)
            
            #Writing to file
            file.write('"{}";"{}";"{}";"{}";"{}"\n'.format(
                port, vlan, mac, vendor, macs_on_port)
                       )
        except IndexError:
            pass

tn.close()
