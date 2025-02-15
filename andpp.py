import fire
import os
from scapy.all import sniff, sendp, Ether, IPv6, ICMPv6ND_NS, ICMPv6ND_NA, ICMPv6NDOptDstLLAddr, get_if_hwaddr

ns_counter=0
def dump_nd_so(x):
    global ns_counter
    ns_counter+=1
    return x.sprintf(rf"NS({ns_counter}) >> ether src:%Ether.src%->ether dst:%Ether.dst% ipv6 src:%IPv6.src%->ipv6 dst:%IPv6.dst% ns tgt:%ICMPv6ND_NS.tgt% options-lladdr:%ICMPv6NDOptSrcLLAddr.lladdr%")

na_counter=0
def dump_nd_ad(x):
    global na_counter
    na_counter+=1
    return x.sprintf(rf"NA({na_counter}) >> ether src:%Ether.src%->ether dst:%Ether.dst% ipv6 src:%IPv6.src%->ipv6 dst:%IPv6.dst% na tgt:%ICMPv6ND_NA.tgt% options-lladdr:%ICMPv6NDOptDstLLAddr.lladdr%")

def send_nd_ad_for(x, outer_ether_addr):
    ether_dst = x[Ether].src
    iface = x.sniffed_on
    ether_src=outer_ether_addr
    sendp(Ether(dst=ether_dst, src=ether_src)/IPv6(version=6, tc=0, fl=0, plen=32, hlim=255, src=x[ICMPv6ND_NS].tgt, dst=x[IPv6].src)/ICMPv6ND_NA(code=0, R=0, S=1, O=1, res=0x0, tgt=x[ICMPv6ND_NS].tgt)/ICMPv6NDOptDstLLAddr(type=2, len=1, lladdr=outer_ether_addr), iface=iface)
    return True

def is_expected_nd_so(x, expected_prefix):
    return x[ICMPv6ND_NS].tgt.startswith(expected_prefix)

def is_expected_nd_ad(x, expected_prefix):
    return x[ICMPv6ND_NA].tgt.startswith(expected_prefix)

def main(outer_iface, proxy_net_prefix):
    outer_ether_addr=get_if_hwaddr(outer_iface)
    sniff(filter='icmp6',
          lfilter= lambda x: is_expected_nd_so(x, proxy_net_prefix) if ICMPv6ND_NS in x else is_expected_nd_ad(x, proxy_net_prefix) if ICMPv6ND_NA in x else False,
          prn= lambda x: (dump_nd_so(x),send_nd_ad_for(x, outer_ether_addr))[0] if ICMPv6ND_NS in x else dump_nd_ad(x),
          iface=outer_iface)

if __name__ == '__main__':
    fire.Fire(main)
