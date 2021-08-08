#!/usr/bin/env python
import logging
import datetime
import winrm
from winrm.protocol import Protocol


def process(event, mydb):
    # NTLMv2 vulnerable to MITM & replay
    # Fork mitigations so they can occur in parallel?
    logging.basicConfig(filename='/soar/mitigation/daemon.log', encoding='utf-8', level=logging.DEBUG)
    p = Protocol(
            endpoint='http://' + event['host'] + ':5985/wsman',
            transport='ntlm',
            username=r'domain\useraccount',
            password='password',
            server_cert_validation='ignore')
    try:
        shell_id = p.open_shell()
    except:
        logging.info(str(datetime.datetime.now()) + ' failed to login and mitigate ' + event['host'])
        return
    command = p.run_command(shell_id, 'powershell.exe -Command "& {Disable-NetAdapter -Name * -Confirm:$false}"')
    std_out, std_err, status_code = p.get_command_output(shell_id, command)
    logging.info(str(datetime.datetime.now()) + ' disabled network adapters on ' + event['host'])
    p.cleanup_command(shell_id, command)
    p.close_shell(shell_id)
    mydb.mark_read(event['_id'], "actions") # Mark action as mitigated
    doc = {'type': 'email', 'read': 0, 'message': 'The network adapters on ' + event['host'] + ' have been disabled due to a significant malware detection'}
    mydb.insert(doc, "actions") # Send email alert that a host was quarantined
    logging.info(str(datetime.datetime.now()) + ' Finished processing WinRM plugin')

def init(mydb):
    for x in mydb.query({"read": 0, "type": "winrmquarantine"}, "actions"):
        try:
            process(x, mydb) # Process the event data
        except:
            logging.info(str(datetime.datetime.now()) + ' error processing event id ' + str(x['_id']))
