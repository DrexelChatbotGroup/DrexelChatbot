"""
Entry point for the Information extraction component
"""

__all__ = []
__version__ = '0.2'
__author__ = 'Tom Amon'

from ieagents import *
from database import stardog

_DATABASE_NAME = "chatbotDB"

def _main():
    agents = []
    agents.append(cci_ieagent.CciIEAgent())
    agents.append(coas_ieagent.CoasIEAgent())
    agents.append(lebow_ieagent.LebowIEAgent())
    agents.append(biomed_ieagent.BiomedIEAgent())
    ttl_files = []

    for agent in agents:
        ttl = agent.write_ttl()
        ttl_files.append(ttl.filename)

    try:
        db = stardog.StardogDB(_DATABASE_NAME)
        d.remove_all()
        db.add(ttl_files)
    except TypeError:
        print("Failed! Is the database %s running?" % _DATABASE_NAME)

if __name__ == "__main__":
    _main()
