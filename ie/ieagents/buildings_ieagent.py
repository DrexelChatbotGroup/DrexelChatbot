"""
Implementation of the IEAgent interface for all buidlings. 
This simply reads the csv file buildings_info.csv 
"""

__all__ = ['BuildingsIEAgent']
__version__ = '0.1'
__author__ = 'Tom Amon'

import abc
from .ieagent import IEAgent
import ttl
import csv

class BuildingsIEAgent(IEAgent):
    csv_filename = "building_info.csv"
    ttl_filename = "ttl/buildings.ttl"

    def write_ttl(self):
        with open(self.csv_filename, 'r') as f:
            ttl_file = ttl.TtlFile(self.ttl_filename)
            reader = csv.DictReader(f)
            for row in reader:
                building = ttl.TtlFileEntry()
                building.property = "building"

                names = row["Name"]
                names = names.split(';')
                building.name = names[0]
                building.altnames = names[1:]
                if(row["Code"]):
                    building.altnames.append(row["Code"])
                    building.altnames.append(row["Code"].title())

                building.department = row["Function"]
                building.address = row["Address"]
                building.picture = row["Picture"]
                building.website = row["Website"]

                building.mStartTime = row["MStartTime"]
                building.tStartTime = row["MStartTime"]
                building.wStartTime = row["MStartTime"]
                building.thStartTime = row["MStartTime"]
                building.fStartTime = row["MStartTime"]
                building.saStartTime = row["MStartTime"]
                building.suStartTime = row["MStartTime"]
                building.mEndTime = row["MEndTime"]
                building.tEndTime = row["MEndTime"]
                building.wEndTime = row["MEndTime"]
                building.thEndTime = row["MEndTime"]
                building.fEndTime = row["MEndTime"]
                building.saEndTime = row["MEndTime"]
                building.suEndTime = row["MEndTime"]

                building.write_to(ttl_file)
    
            ttl_file.close()
            return ttl_file
