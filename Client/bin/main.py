#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#date:2018-02-28
#function:

__author__ = 'xiaoshouhua'

import os
import sys

BASE_DIR = os.path.dirname(os.getcwd())
sys.path.append(BASE_DIR)

from core import handler

if __name__ == '__main__':
    handler.ArgvHandler(sys.argv)

