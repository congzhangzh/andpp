# Another NDP Proxy(andpp)
Turn a none routeable ipv6 subnet to routeable

# Requirements
1. Python 3.x
2. Scapy
3. Google Fire

## For conda
```bash
conda create -n andpp python
conda activate andpp
pip install fire scapy
```

## For Debian
```bash
sudo aptitude install python3-fire python3-scapy
```

# Usage
Run the script from the command line, providing necessary parameters:

```bash
sudo python3 andpp.py outer_iface outer_ether_addr router_ether_addr proxy_net_prefix

# you can add to your cron table by crontab -e like:
# @reboot sleep 120; sudo python3 ~/projects/andpp/andpp.py eth0 00:11:31:f1:01:71 44:22:22:33:3a:00 2a03:dddd:a11f:
```

## Parameters
outer_iface:

    The outer interface to use (e.g., ens11 or eth0). get from:
```bash
    ip link
```

outer_ether_addr:

    The Ethernet address for the outer interface (e.g., xx:xx:xx:xx:xx:xx).
```bash
    ip link
```

router_ether_addr: 

    The Ethernet address for the router (e.g., xx:xx:xx:xx:xx:xx).

```bash
    ip -6 neighbor
```

proxy_net_prefix: 

    The proxy network prefix (e.g., xxxx:xxx:xxx:xxx:). 
    
    This should get from you ISP!
