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
                names = names + self.filter_common_names(names)

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
                building.tStartTime = row["TStartTime"]
                building.wStartTime = row["WStartTime"]
                building.thStartTime = row["ThStartTime"]
                building.fStartTime = row["FStartTime"]
                building.saStartTime = row["SaStartTime"]
                building.suStartTime = row["SuStartTime"]
                building.mEndTime = row["MEndTime"]
                building.tEndTime = row["TEndTime"]
                building.wEndTime = row["WEndTime"]
                building.thEndTime = row["ThEndTime"]
                building.fEndTime = row["FEndTime"]
                building.saEndTime = row["SaEndTime"]
                building.suEndTime = row["SuEndTime"]

                building.write_to(ttl_file)
    
            ttl_file.close()
            return ttl_file

    def filter_common_names(self, names):
        common_words = ["Building", "Hall"]
        new_names = []
    
        for n in names:
            words = n.split()
            last_word = words[len(words)-1]
            if last_word in common_words:
                new_names.append(n[:-len(last_word)])

        return new_names
