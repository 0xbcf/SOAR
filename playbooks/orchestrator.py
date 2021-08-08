#!/usr/bin/env python
import os, sys, time
from service import Service
from mydb import mydb
import datetime,logging

# Import production modules here
# from [folder] import [class]
from malware_triage import malware_triage

class MyService(Service):
    def run(self):
        logging.basicConfig(filename='/soar/playbooks/daemon.log', encoding='utf-8', level=logging.DEBUG)
        logging.info(str(datetime.datetime.now()) + ' daemon started')
        dbcon = mydb() # Initiate the database
        while not self.got_sigterm():
                # Process the playbooks
                # List all active playbooks below
                malware_triage.init(dbcon)

                # End of active playbooks
                time.sleep(10) # sleep for 15 seconds

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Syntax: %s [start|stop|status]' % sys.argv[0])
    cmd = sys.argv[1].lower()
    service = MyService('orchestrator.py', pid_dir='/tmp')
    if cmd == 'start':
        print("Starting service..")
        service.start()
    elif cmd == 'stop':
        service.stop()
        print("Stopping service..")
    elif cmd == 'status':
        if service.is_running():
            print("Service is running")
        else:
            print("Service is not running")
    else:
        sys.exit('Unknown command "%s".' % cmd)
