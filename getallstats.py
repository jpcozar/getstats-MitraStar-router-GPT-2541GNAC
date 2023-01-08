# File: getallstats.py
# Author: Javier Polo Cozar
# Date: Jan-2021
# Description: Get statistics (Bytes and Packets of any Interface LAN orWAN) from a MitraStar Router

# Libs needed to do expect to router
import sys
import pexpect


arguments = len(sys.argv)-1
if (arguments < 4):
    print("4 arguments are needed: user, IP router, password, filename")
else:
    user = sys.argv[1]
    IP = sys.argv[2]
    password = sys.argv[3]
    filename=sys.argv[4]

# From OpenSSH 8.8 we need to add -o HostKeyAlgorithms=+ssh-rsa
# PubkeyAcceptedAlgorithms=+ssh-rsa

    child = pexpect.spawn('ssh -oHostKeyAlgorithms=+ssh-rsa -oStrictHostKeyChecking=no ' + user + '@' + IP)
    child.expect(user + '@' + IP + "'s password: ")
    child.sendline(password)
    child.expect(' fail to read file > ')
    child.sendline('showlanstats')
    child.expect('> ')
    cmd_show_data=child.before
    child.sendline('showwanstats')
    child.expect('> ')

    cmd_show_data += child.before
    cmd_show_data_decoded = cmd_show_data.decode('utf-8')
    cmd_output = cmd_show_data_decoded.split('\r\n')
    temp = sys.stdout
    with open(filename, 'w') as f:
        sys.stdout = f
        for data in cmd_output:
            print(data)
    child.sendline("exit")
    sys.stdout.close()
    sys.stdout = temp
