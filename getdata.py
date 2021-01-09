# File: getdata
# Author: Javier Polo Cozar
# Description: get individual data statistics
# Parameters: filename, interface, tx|rx, B(ytes), P(ackets), E(rrors), D(rops)
# Date: Jan-2021
# Add compatibility with pyhton3

import sys

arguments = len(sys.argv) - 1
if (arguments < 4):
    print("4 Arguments are needed: Filename, interface, tx|rx, B(tyes)|P(ackets)|E(rrors)|D(rops)")
else:
    getdata = False
    data = sys.argv[4]
    filename = sys.argv[1]

    with open(filename) as origin_file:
        if (sys.argv[3] == "rx"):
            recibido = True
        else:
            recibido = False

        for line in origin_file:
            if not sys.argv[2] in line:
                continue
            try:
                line = line.split()
                if (recibido):
                    if (data == "B"):
                        print(line[2])
                    if (data == "P"):
                        print(line[3])
                    if (data == "E"):
                        print(line[4])
                    if (data == "D"):
                        print(line[5])
                    break
                else:
                    if (getdata == False):
                        getdata = True
                    else:
                        if (data == "B"):
                            print(line[2])
                        if (data == "P"):
                            print(line[3])
                        if (data == "E"):
                            print(line[4])
                        if (data == "D"):
                            print(line[5])
                        break
            except IndexError:
                print
