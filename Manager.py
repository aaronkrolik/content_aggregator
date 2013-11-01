'''
Created on Sep 20, 2013

@author: aaronkrolik
'''
from plugins import *

x = Plugin.returnListOfInstances()

for instance in x:
    instance.showMichaelThisWorks()