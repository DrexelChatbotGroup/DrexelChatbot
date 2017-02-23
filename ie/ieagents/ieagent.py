"""
Interface for all classes that will get data from a single website. 
"""

__all__ = ['IEAgent']
__version__ = '0.1'
__author__ = 'Tom Amon'

import abc

class IEAgent(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def refresh(self, database):
        """refresh the database"""
        return
