"""
Entry point for the Information extraction component
"""

__all__ = []
__version__ = '0.2'
__author__ = 'Tom Amon'

from ieagents import *
from database import stardog
import sys
import getopt

_DATABASE_NAME = "chatbotDB"

def _main(argv):

    try:
        opts, args = getopt.getopt(argv,"htd",[])
    except getopt.GetoptError:
        print('iemain.py [OPTION]')
        sys.exit(2)

    ttl_gen = True 
    db_refresh = True
    for opt, arg in opts:
        if opt == '-h':
            print('iemain.py [OPTION]')
            print('-t   just generate ttl files')
            print('-d   just refresh the database')
            sys.exit()
        elif opt == "-t":
            db_refresh = False
        elif opt == "-d":
            ttl_gen = False

    agents = []

#    agents.append(cci_ieagent.CciIEAgent())
#    agents.append(coas_ieagent.CoasIEAgent())
#    agents.append(lebow_ieagent.LebowIEAgent())
#    agents.append(biomed_ieagent.BiomedIEAgent())
#    agents.append(westphal_ieagent.WestphalIEAgent())
    agents.append(ece_ieagent.EceIEAgent())

    ttl_files = []
    for agent in agents:
        ttl_files.append(agent.ttl_filename)

    if ttl_gen:
        _generate_ttls(agents)
    if db_refresh:
        _refresh_db(ttl_files)

    print("Done.")

def _generate_ttls(agents):
    for agent in agents:
        ttl = agent.write_ttl()
        print("Wrote %s" % ttl.filename)

def _refresh_db(ttl_files):
    try:
        db = stardog.StardogDB(_DATABASE_NAME)
        print("Clearing database %s" % _DATABASE_NAME)
        db.remove_all()
        print("Adding files to database %s" % _DATABASE_NAME)
        db.add(ttl_files)
    except TypeError:
        print("Failed! Is the database %s running?" % _DATABASE_NAME)
        print(T)

if __name__ == "__main__":
    _main(sys.argv[1:])
