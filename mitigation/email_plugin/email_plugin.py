#!/usr/bin/env python
import logging
import datetime
import smtplib
from email.mime.text import MIMEText

def process(event, mydb):
    logging.basicConfig(filename='/soar/mitigation/daemon.log', encoding='utf-8', level=logging.DEBUG)
    try:
        smtpObj = smtplib.SMTP('smtprelay')
        message = """To: DestinationEmail\nSubject: [Security automation] System Quarantined\n
        The security automation system has been activated and generated the following message:
        %s
        """ % (event["message"])
        smtpObj.sendmail("SourceEmail","DestinationEmail",message)
        smtpObj.quit()
        logging.info(str(datetime.datetime.now()) + ' sent email notice')
    except:
        logging.info(str(datetime.datetime.now()) + ' failed to send email notice')
        return
    mydb.mark_read(event['_id'], "actions") # Mark action as mitigated

def init(mydb):
    logging.basicConfig(filename='/soar/mitigation/daemon.log', encoding='utf-8', level=logging.DEBUG)
    for x in mydb.query({"read": 0, "type": "email"}, "actions"):
        try:
            process(x, mydb) # Process the event data
        except:
            logging.info(str(datetime.datetime.now()) + ' error processing event id ' + str(x['_id']))
