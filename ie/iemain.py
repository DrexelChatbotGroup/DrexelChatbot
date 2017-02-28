"""
Entry point for the Information extraction component
"""

__all__ = []
__version__ = '0.1'
__author__ = 'Tom Amon'

from ieagents import *

def _main():
    agents = []
    agents.append(cci_ieagent.CciIEAgent())
    agents.append(coas_ieagent.CoasIEAgent())
    database = None

    for agent in agents:
        agent.refresh(database)

if __name__ == "__main__":
    _main()
