# Another NDP Proxy(andpp)
Turn a none routeable ipv6 subnet to routeable

# Requirements
1. Python 3.x
2. Scapy
3. Google Fire

## For some local env like venv or conda
```bash
pip install fire scapy
```

## For debian os
```bash
sudo aptitude install python3-fire python3-scapy
```

# Usage
Run the script from the command line, providing necessary parameters:

```bash
python andpp.py --outer_iface=ensx --outer_ether_addr=xx:xx:xx:xx:xx:xx --router_ether_addr=xx:xx:xx:xx:xx:xx --proxy_net_prefix=xxxx:xxx:xxx:xxx:
```

## Parameters
--outer_iface: 
    The outer interface to use (e.g., ens11 or eth0).

--outer_ether_addr: 
    The Ethernet address for the outer interface (e.g., xx:xx:xx:xx:xx:xx).

--router_ether_addr: 
    The Ethernet address for the router (e.g., xx:xx:xx:xx:xx:xx).

--proxy_net_prefix: 
    The proxy network prefix (e.g., xxxx:xxx:xxx:xxx:).
