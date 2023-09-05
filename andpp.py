outer_iface='ensx|ethx'
outer_ether_addr='xx:xx:xx:xx:xx:xx'
router_ether_addr='xx:xx:xx:xx:xx:xx'

proxy_net_prefix='xxxx:xxx:xxx:xxx:'

def dump_nd_so(x):
    return x.sprintf("ether src:%Ether.src%->ether dst:%Ether.dst% ipv6 src:%IPv6.src%->ipv6 dst:%IPv6.dst% ns tgt:%ICMPv6ND_NS.tgt% options-lladdr:%ICMPv6NDOptSrcLLAddr.lladdr%")
    pass

def dump_nd_ad(x):
    return x.sprintf("ether src:%Ether.src%->ether dst:%Ether.dst% ipv6 src:%IPv6.src%->ipv6 dst:%IPv6.dst% na tgt:%ICMPv6ND_NA.tgt% options-lladdr:%ICMPv6NDOptDstLLAddr.lladdr%")
    pass

def send_nd_ad_for(x, iface, ether_src, ether_dst):    
    sendp(Ether(dst=ether_dst, src=ether_src)/IPv6(version=6, tc=0, fl=0, plen=32, hlim=255, src=x[ICMPv6ND_NS].tgt, dst=x[IPv6].src)/ICMPv6ND_NA(code=0, R=0, S=1, O=1, res=0x0, tgt=x[ICMPv6ND_NS].tgt)/ICMPv6NDOptDstLLAddr(type=2, len=1, lladdr=outer_ether_addr), iface=iface)
    return True
    pass

def is_expected_nd_so(x, expected_prefix):
    return x[Ether].src==router_ether_addr and x[ICMPv6ND_NS].tgt.startswith(expected_prefix)
    pass

def is_expected_nd_ad(x, expected_prefix):
    return x[Ether].dst==router_ether_addr and x[ICMPv6ND_NA].tgt.startswith(expected_prefix)
    pass

sniff(filter='icmp6', lfilter= lambda x: is_expected_nd_so(x, proxy_net_prefix) if ICMPv6ND_NS in x else is_expected_nd_ad(x, proxy_net_prefix) if ICMPv6ND_NA in x else False, prn= lambda x: (dump_nd_so(x),send_nd_ad_for(x, outer_iface, outer_ether_addr, router_ether_addr))[0] if ICMPv6ND_NS in x else dump_nd_ad(x), iface=outer_iface)
