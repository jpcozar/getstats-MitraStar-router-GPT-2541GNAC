# getstats-MitraStar-router-GPT-2541GNAC
Getting stats from MitraStar GPT-2541 GNAC router for using them in Home Assistant

# Synopsis
We use expect (via pexpect in python) to connect to router and get lan|wan statistics of MitraStar GPT-2541GNAC router. There are two files:
1. `getallstats.py`: connect to router and get a txt file with stats
1. `getdata.py`: open stats file and get stat we want: 
* **LAN | WAN**
* **Interface**: ethX, veip0.x, ppp0.x
* **Transmitted | Received**
* **Bytes | Packets | Errors | Drops**

# Motivation
As UPnP integration of Home Assistant wasn't working for MitraStar GPT-2541 GNAC router, I have created these scripts to get statistics from router.

## Requirements
We need **pexpect** python library and **python 3.x** installed in order to work. python3 is installed by default in Hassio. We can install `pexpect` with `pip`:
### Installing pexpect
`pip install pexpect`

## Configuration: Exchanging keys
We need to do a first manual ssh sesion with router to get key of router and add it to known hosts file so it isnt asked again, before expect (pexect) can work. Somethign like that:

`ssh <user>@<router IP>`

For example:

        ssh 1234@192.168.1.1
        The authenticity of host '192.168.1.1 (192.168.1.1)' can't be established.
        RSA key fingerprint is SHA256:NGxis9N+wLGUWNCJHixmk5tfU7NOC+3PITfYrDnXooQ.
        Are you sure you want to continue connecting (yes/no)? yes
        Warning: Permanently added '192.168.1.1' (RSA) to the list of known hosts.
        1234@192.168.1.1's password:
         fail to read file > exit

        Bye bye. Have a nice day!!!

## Execution: getting statistics file
`python3 getallstats.py <router user> <router IP> <router password> <filename txt>`

For example:
`python3 getallstats.py 1234 192.168.1.1 4321 lanwanstats.txt`

it will create a file called **lanwnstats.txt** like that one, with LAN and WAN stats for every interface we have:

        showlanstats
        Received Counters:
        Interface Status    Total                                  Multicast           Unicast Broadcast
                            Bytes       Pkts       Errs    Drops   Bytes       Pkts    Pkts    Pkts
             eth0 Disabled  0           0          0       0       0           0       0       0      
             eth1 Up        1429072538  16890206   0       0       0           11248703 5609300 32203  
             eth2 Up        968585382   24175007   0       0       0           305830  23594954 274223 
             eth3 Up        1272700034  26847309   0       0       0           354008  26279470 213831 
             eth4 Up        505759232   20495071   0       0       0           385883  20087272 21916  

        Transmitted Counters:
        Interface Status    Total                                  Multicast           Unicast Broadcast
                            Bytes       Pkts       Errs    Drops   Bytes       Pkts    Pkts    Pkts
             eth0 Disabled  0           0          0       0       0           0       0       0      
             eth1 Up        2383593974  229496149  0       0       0           167279947 60931963 1284239
             eth2 Up        1662544234  31800348   0       0       0           1057913 29653628 1088807
             eth3 Up        2406961079  27571438   0       0       0           914373  25552910 1104155
             eth4 Up        3858697336  29671073   0       0       0           1547093 25831738 2292242
         showwanstats
        Received Counters:
        Interface VlanMuxId   Total                                  Multicast           Unicast Broadcast
                              Bytes       Pkts       Errs    Drops   Bytes       Pkts    Pkts    Pkts
          veip0.2         3   35274591    187101     0       0       846872      16286   170815  0      
          veip0.3         2   1953339658  44180817   0       0       0           294194  43886623 0      
           ppp0.1         6   2294911201  1646628073 0       0       0           0       1646628073 0      

        Transmitted Counters:
        Interface VlanMuxId   Total                                  Multicast           Unicast Broadcast
                              Bytes       Pkts       Errs    Drops   Bytes       Pkts    Pkts    Pkts
          veip0.2         3   37778418    171027     0       0       0           0       171027  0      
          veip0.3         2   3364100707  6191552    0       0       0           0       6191552 0      
           ppp0.1         6   1370104568  1667200174 0       0       0           0       1667200174 0
           
**We should do a task to re-create this file periodically. (I am doing a crontab job every minute).**

## Getting individual stat: getdata.py
We get individual stat with `getdata.py` with this syntax:

`python3 getdata.py <filename> <interface> <rx|tx> <B|P|E|D>`

1. **`<filename>`**: name of file generated with `getallstats.py`
1. **`<tx | rx>`**: we get Transmitted or Received stat
1. **`<B | P | E | D>`**: we get B(ytes), P(ackets), E(rrors), D(rops).

For example:

`python3 getdata.py lanwanstats.txt veip0.2 tx B`

 `37778418` 

We would get the transmitted Bytes in the interface veip0.2 (wan).

# Home Assistant configuration
We create a directory in config dir: 

`\\<HA IP>\config\python-scripts\getstats`

This directory must contain **`getdata.py`** and **lanwanstats.txt** generated periodically by `getallstats.py`

So we can edit `configuration.yaml` and add a sensor like that one:

    sensor:
       - platform: command_line
           name: WAN VozIP (veip0.2) KBytes tx
           command: 'python3 /config/python-scripts/getstats/getdata.py /config/python-scripts/getstats/lanwanstats.txt veip0.2 tx B'
           unit_of_measurement: "KBytes"
           value_template: '{{value|multiply (0.001)}}'


