#!/usr/bin/env python
import logging
import datetime
from netmiko import ConnectHandler


def process(event, mydb):
    logging.basicConfig(filename='/soar/mitigation/daemon.log', encoding='utf-8', level=logging.DEBUG)
    cisco_asa = {
            'device_type': 'cisco_ios',
            'host': 'firewall',
            'username': 'useraccount',
            'password': 'password',
            'port': 22,
            'secret': 'enable_password',
            }
    net_connect = ConnectHandler(**cisco_asa)
    net_connect.enable()
    config_commands = ['object-group network Automated_Blacklist',
            'network-object host ' + event['host']]
    output = net_connect.send_config_set(config_commands)
    logging.info(str(datetime.datetime.now()) + output)
    net_connect.save_config()
    net_connect.disconnect()
    mydb.mark_read(event['_id'], "actions") # Mark action as mitigated

def init(mydb):
    logging.basicConfig(filename='/soar/mitigation/daemon.log', encoding='utf-8', level=logging.DEBUG)
    for x in mydb.query({"read": 0, "type": "firewallblock"}, "actions"):
        try:
            process(x, mydb) # Process the event data
        except:
            logging.info(str(datetime.datetime.now()) + ' error processing event id ' + str(x['_id']))
