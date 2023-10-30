# -*- coding: utf-8 -*-
"""
Created on Sat Sep  23 16:31:55 2023

@author: ashwe
"""

# importing all required libraries
import logging as lg
import os, sys
from datetime import datetime
import gvars

from telethon.sync import TelegramClient
from telethon import TelegramClient

global teleerr
teleerr = None

def Logtotelegram(msg):
    global teleerr
    if(gvars.log_tel):
        try:
            if(gvars.isAuth):
                gvars.client.send_message(gvars.receiver, msg, parse_mode='html')
        except Exception as err:
            print(err)
            teleerr = err
            gvars.isAuth = False

class MyStreamHandler(lg.Handler):
    terminator = '\n'
    def __init__(self):
        lg.Handler.__init__(self)
        self.stream = sys.stdout
    def emit(self, record):
        if (record.levelno == lg.INFO or record.levelno == lg.WARNING or record.levelno == lg.ERROR):
            try:
                msg = self.format(record)
                stream = self.stream
                stream.write(msg + self.terminator)
                self.flush()
                Logtotelegram(msg)
            except RecursionError:
                raise
            except Exception:
                self.handleError(record)

def initialize_logger():
    global teleerr

    # creating s folder for the log
    logs_path = './logs/'
    try:
        os.mkdir(logs_path)
    except OSError:
        print('Creation of the directory %s failed - it does not have to be bad' % logs_path)
    else:
        print('Succesfully created log directory')

    # renaming each log depending on time Creation
    date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    gvars.filename = date_time + '_report.csv'
    log_name = date_time + '.log'
    log_name = 'logger_file.log'
    currentLog_path = logs_path + log_name

    # log parameter
    lg.basicConfig(filename = currentLog_path, format = '%(asctime)s {%(pathname)s:%(lineno)d} [%(threadName)s] - %(levelname)s: %(message)s', level = lg.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

    # print the log in console
    # console_formatter = lg.Formatter("%(asctime)s {%(pathname)s:%(lineno)d} [%(threadName)s] - %(levelname)s: %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    console_formatter = lg.Formatter("%(asctime)s : %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    console_handler = MyStreamHandler()
    console_handler.setFormatter(console_formatter)
    
    # lg.getLogger().addHandler(lg.StreamHandler())
    lg.getLogger().addHandler(console_handler)

    # sending log msg to telegram
    if(gvars.log_tel):
        try:
            gvars.client = TelegramClient('session', gvars.api_id, gvars.api_hash)
            gvars.client.connect()
            if not gvars.client.is_user_authorized():
                gvars.client.send_code_request(gvars.phone)
                gvars.client.sign_in(gvars.phone, input('Enter the code: '))
        except Exception as err:
            teleerr = err

        if gvars.client.is_user_authorized():
            gvars.isAuth = True
        else:
            gvars.isAuth = False

    # init message
    lg.info('Log initialized')

    if teleerr is not None:
        lg.error(teleerr)
