'''
Created on Sep 20, 2013

@author: aaronkrolik
'''
import time


class metaPlugin(type):
    def __init__(cls, name, bases, namespace):
        super(metaPlugin, cls).__init__(name, bases, namespace)
        if not hasattr(cls, '_metaPlugin__directory'):
            cls.__directory = {}
        cls.__directory[name] = cls
        
        #if len(bases)>0:
             
    def printDirectory(self):
        if hasattr(self, "_metaPlugin__directory"):
            print self.__directory
            
    def returnClass(self, name):
        if hasattr(self, "_metaPlugin__directory") and name in self.__directory:
            return self.__directory[name]
        
    def returnInstance(self, name):
        return self.returnClass(name)()
            
    def returnListOfInstances(self):
        if hasattr(self, "_metaPlugin__directory") and self.__directory != None:
            return [self.returnInstance(name) for name in self.__directory.keys()]
        

    

class Plugin:
    __metaclass__ = metaPlugin
    
    def retreiveData(self, *args, **kwargs):
        pass
    
    def formatJSONStrForSolrIndexing(self, *args, **kwargs):
        pass
    #Taken from StackOverflow
    def getEpoch(self):
        date_time = '29.08.2011 11:05:02'
        pattern = '%d.%m.%Y %H:%M:%S'
        return time.time()
    
    def run(self):
        pass








