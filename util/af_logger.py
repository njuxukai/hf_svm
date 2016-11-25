# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 14:05:35 2015

@author: xukai
"""

import logging
import logging.config

logging.config.fileConfig("logger.conf")
logger = logging.getLogger("Global")