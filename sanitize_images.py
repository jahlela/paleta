#!/usr/bin/python

import os, sys



os_path = os.path.dirname(os.path.abspath(__file__))

from path import path
d = path(os_path + '/static/img/photos/')
print 'directory', d
#replace directory with your desired directory
for i in d.walk():
    if i.isfile():
        print i.name
        # if i.name == 'php.py':
        #     i.remove()