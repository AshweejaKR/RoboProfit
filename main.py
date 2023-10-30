# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 19:22:16 2023

@author: ashwe
"""

# importing all required libraries
from logger import *
import gvars
# from SmartApi import SmartConnect
from pyotp import TOTP
import urllib
import json

def main():
    # initialize the logger (imported from logger)
    initialize_logger()

    lg.info('Trading Bot running ... !')


    lg.info('Trading Bot finished ... ')

if __name__ == '__main__':
    main()