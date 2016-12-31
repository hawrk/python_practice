__author__ = 'hawrk'
__date__ = '2016.08.01'
'test python logging module'

# -*- coding: utf-8 -*-
import logging
import multiprocessing

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%d %b %Y %H:%M:%S',
                    filename='pylog.log',
                    filemode='a')
logging.debug('*************begin*******************')
logging.debug('this message should go to the log file')
logging.info('so should this')
logging.warning("watch out!")

logging.info("I told you so")


print (r'tes\n\r\'kkk')

def my_fun():
    pass