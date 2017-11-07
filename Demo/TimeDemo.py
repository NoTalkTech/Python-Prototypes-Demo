#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import logging
import time

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    t = time.time()
    logger.info("Time: {} seconds.".format(t))
    logger.info("GMTime: {} ".format(time.gmtime(t)))
    logger.info("LocalTime: {} ".format(time.localtime(t)))
    logger.info("DateTimeNow: {} ".format(datetime.datetime.now()))
    logger.info("DataTimeUTCNow: {} ".format(datetime.datetime.utcnow()))
