copyright='copyright 2022 r.kras'
import argparse
import json
import sys

from dns.resolver import Resolver
from sender_policy_flattener.crawler import spf2ips

from .cf_dns import TXTrec

version_info=f'{sys.argv[0].split("/")[-1]}  0.1 {copyright}'

            
def runflat(domain, nameservers=None, senders={}):
    """ Run flattener from sender-policy-flattener"""

    resolver = Resolver()
    if nameservers:
        resolver.nameservers = nameservers

    records = spf2ips(senders, domain, resolver)
    
    return records


def getconfig(fname):
    """ Open and load json config file """
    
    with open(fname, 'rb') as f:
        return json.load(f)
    

def args_parse():
    """ Parse command line arguments """

    parser = argparse.ArgumentParser(
        description='Flatten and update Cloudflare SPF records', epilog=f'\n{version_info}\n')

    parser.add_argument('-u','--update', help='Update the Cloudflare zone SPF records', action='store_true', default=False)
    parser.add_argument('-c','--config', help='Config filename', required=True)
    
    args = parser.parse_args()

    return args


def cf_flatten(config,update):
    """ load config and run flattener"""
    
    cfg = getconfig(config)
    zone = cfg['cf_zone']

    if update:
        spfs = TXTrec(zone)
    
    nameservers = cfg.get('resolvers',[])
    sending_domains = cfg['sending domains']

    for domain in sending_domains:
        senders = sending_domains[domain]
        
        records = runflat(domain, nameservers, senders )
        print(f'\n**** Flattened SPF Records for {domain} ****\n')        
        
        numrecs = len(records)
        for i in range(0,numrecs):
            recname = f'spf{i}.{domain}'
            print(f'{recname} => "{records[i]}"\n')
            if update:
                print(f'=======>Setting {recname} in {zone}\n')
                spfs.set(recname, records[i])
        
        if update:
            print(f'\n**** {numrecs} SPF records have been updated in {zone}\n')
        else:
            print('\n**** IMPORTANT ****\nNo changes were made (use the --update flag to update Cloudflare records)\n')

 
def main(args=None):
    """ Run """
    if not args:
        args = args_parse()

    cf_flatten(config=args.config, update=args.update)

