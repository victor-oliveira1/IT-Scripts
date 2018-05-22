#!/bin/python3
#Get MAC addresses via telnet from managed switches
import telnetlib
import sys
import re

user = 
password = 
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
        Send()
        tmp = Read('---- More ----')
        maclist += tmp
    else:
        break

print('Writing file...')
with open(host + '.csv', 'w') as file:
    for line in maclist.split('\n'):
        try:
            #Removing weird strings
            line = re.findall('\w{4}-\w{4}-\w{4}.*', line)[0]
            #Removing More string
            line = line.replace('---- More ----', '')
            #Joining all together
            line = ';'.join(line.split())
            #Writing to file
            file.write(line + '\n')
        except:
            pass

tn.close()
