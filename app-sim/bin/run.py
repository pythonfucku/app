#!/bin/env python
# encoding:utf-8
'''
#=============================================================================
#     FileName: run.py
#         Desc: Æô¶¯º¯Êý
#       Author: Crow
#        Email: lrt_no1@163.com
#     HomePage: @_@"
#      Version: 1.0.0
#   LastChange: 2016-08-11 15:59:30
#      History:
#=============================================================================
'''

import os
import sys
sys.path.append(os.path.join(os.path.split(sys.path[0])[0],"src"))

from lib.core.main import main

if __name__ == "__main__":
    app = main()

