#!/usr/bin/env python
import os, sys, time
from service import Service
from mydb import mydb
import datetime, logging


# Import production mitigation modules here
from winrm_plugin import winrm_plugin
from email_plugin import email_plugin
from firewall_plugin import firewall_plugin


class MyService(Service):
    def run(self):
        logging.basicConfig(filename='/soar/mitigation/daemon.log', encoding='utf-8', level=logging.DEBUG)
        logging.info(str(datetime.datetime.now()) + ' daemon started')
        dbcon = mydb() # Initialize the database connection
        while not self.got_sigterm():
            # Production mitigation modules below
            winrm_plugin.init(dbcon)
            firewall_plugin.init(dbcon)
            email_plugin.init(dbcon)
            # End of production modules
            time.sleep(25)
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Syntax: %s [start|stop|status]' % sys.argv[0])
    cmd = sys.argv[1].lower()
    service = MyService('mitigate.py', pid_dir='/tmp')
    if cmd == 'start':
        print("Starting service..")
        service.start()
    elif cmd == 'stop':
        service.stop()
        print("Stopping service.. (wait 25 seconds)")
    elif cmd == 'status':
        if service.is_running():
            print("Service is running")
        else:
            print("Service is not running")
    else:
        sys.exit('Unknown command "%s".' % cmd)
