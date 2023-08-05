#!python

import argparse
import sys

import asyncio

import async_dnsbl_client

def get_args():

    me = sys.argv[0]
    epilog = f'''\nExamples:
    {me} 1.1.1.1
    {me} -a dnsbl.example.com dnsbl.example.org -r dnsbl.example.net 1.1.1.1'''

    parser = argparse.ArgumentParser(description='Sleep which can awake', epilog=epilog,  formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('host', metavar='HOST', help='host to check (IP or hostname)')
    parser.add_argument('--append', '-a', nargs='+', default=list(), metavar='DNSBL', help='add this DNSBL to check')
    parser.add_argument('--remove', '-r', nargs='+', default=list(), metavar='DNSBL', help='remove this DNSBL')

    return parser.parse_args()

def main():
    args = get_args()
    zones = async_dnsbl_client.dnsbl_zones

    for r in args.remove:
        zones.remove(r)

    zones.extend(args.append)

    result = asyncio.run(async_dnsbl_client.dnsbl(args.host, zones))
    print('\n'.join(result))
    # print(asyncio.run(resolve_with_query('echo.okerr.com')))
    return

    #r = Resolver()
    #r.add_query('google.com')
    #r.add_query('one.one.one.one')
    #r.process()

    resolver = ADNSBL()
    for host in args.host:
        resolver.add_host(host)
    print(args)

if __name__ == '__main__':
    main()