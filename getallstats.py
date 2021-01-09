# Get statistics (LAN|WAN) from a MitraStar Router

import sys
import pexpect

arguments = len(sys.argv)-1
if (arguments < 3):
    print("3 arguments are needed: user, IP router, password")
else:
    user = sys.argv[1]
    IP = sys.argv[2]
    password = sys.argv[3]
    filename = "/volume1/docker/getstats/lanwanstats.txt"
    
    child = pexpect.spawn('ssh ' + user + '@' + IP)
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
