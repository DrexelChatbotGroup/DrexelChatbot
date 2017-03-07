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

    if ttl_gen:
        agents = []
        agents.append(cci_ieagent.CciIEAgent())
        agents.append(coas_ieagent.CoasIEAgent())
        agents.append(lebow_ieagent.LebowIEAgent())
        agents.append(biomed_ieagent.BiomedIEAgent())
        ttl_files = []

        for agent in agents:
            ttl = agent.write_ttl()
            print("Wrote %s" % ttl.filename)
            ttl_files.append(ttl.filename)

    if db_refresh:
        try:
            db = stardog.StardogDB(_DATABASE_NAME)
            print("Clearing database " % _DATABASE_NAME)
            db.remove_all()
            print("Adding files to database " % _DATABASE_NAME)
            db.add(ttl_files)
        except TypeError:
            print("Failed! Is the database %s running?" % _DATABASE_NAME)

    print("Complete!")

if __name__ == "__main__":
    _main(sys.argv[1:])
