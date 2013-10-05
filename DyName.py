#!/usr/bin/python3
"""
VECLabs DyName: Namecoin Dynamic DNS Client
Author: Jeremy Rand AKA biolizard89, Viral Electron Chaos Laboratories
"""

# Bitcoin JSON-RPC API
from jsonrpc.authproxy import AuthServiceProxy

import subprocess
import json
import argparse
import configparser

parser = argparse.ArgumentParser(description='VECLabs DyName: '
                                             'Namecoin Dynamic DNS Client')

parser.add_argument('configfile', help='Configuration File', 
                    metavar='Config.conf')
parser.add_argument('--i-want-my-domain-to-be-stolen', 
                    dest='allow_unsafe_domains', action='store_const', 
                    const=True, default=False, 
                    help='Allows use of d/ names instead of dd/ names.  This '
                         'is a security risk under most circumstances and '
                         'could allow someone to permanently steal control '
                         'of your domain.  Only use this if you really know '
                         'what you\'re doing.')

args = parser.parse_args()

config = configparser.ConfigParser()

config.read(args.configfile)

try:
    namecoind_session = AuthServiceProxy('http://' + 
                                         config['DEFAULT']['RpcUser'] + ':' + 
                                         config['DEFAULT']['RpcPassword'] + 
                                         '@' + config['DEFAULT']['RpcHost'] + 
                                         ':' + config['DEFAULT']['RpcPort'])
    
    print('namecoind is at block ' + str(namecoind_session.getblockcount()) )
except:
    print('Failed to connect to namecoind')

for domain in config:
    
    if str(domain) == 'DEFAULT':
        continue
    
    try:
        name = config[str(domain)]['Name']
        resolver = config[str(domain)]['Resolver']
        source = config[str(domain)]['Source']
        renew_blocks = int(config[str(domain)]['RenewBlocks'])
        #print(name)
        #print(resolver)
        #print(source)
        #print(renew_blocks)
    except:
        print('Skipping domain '+ str(domain) + ' with invalid data')
        continue
    
    if name[:3] != 'dd/' and not args.allow_unsafe_domains:
        print('I will not allow the name ' + name + 
              ' to be stolen without authorization.')
        continue
    
    try:
        current_ip = json.loads(subprocess.check_output(source, 
                                universal_newlines=True))
        #print('Current IP = ' + json.dumps(current_ip))
    except:
        print('Could not get IP address for domain ' + str(domain))
        continue
    
    try:
        expiration = namecoind_session.name_list(name)[0]['expires_in']
    except:
        print('You do not own the name ' + name)
        continue
    
    try:
        old_ip = json.loads(
                 namecoind_session.name_list(name)[0]['value'])[resolver]
        #print('Old IP = ' + json.dumps(old_ip))
    except:
        old_ip = ''
        print('Old IP is nonexistent')
    
    perform_update = False
    
    if json.dumps(current_ip) != json.dumps(old_ip):
        print('Updating IP for domain ' + str(domain))
        perform_update = True
    
    if expiration < renew_blocks:
        print('Renewing domain ' + str(domain))
        perform_update = True
    
    if not perform_update:
        continue
    
    print('New value: ' + '{ "' + resolver + '" : ' + 
                          json.dumps(current_ip) + ' }')
    
    try:
        namecoind_session.name_update(name, '{ "' + resolver + '" : ' + 
                                            json.dumps(current_ip) + ' }')
        print('name_update issued')
    except:
        print("name_update failed for name " + name)
