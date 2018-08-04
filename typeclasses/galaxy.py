# @create/dop myGalaxy:galaxy.Galaxy
# create myGalaxy

from commands.galaxy_commands import GalaxyCmdSet
from evennia import DefaultRoom

class Galaxy(DefaultRoom):
    def at_object_creation(self):
        self.cmdset.add(GalaxyCmdSet, permanent=True)
        
        self.db.system_count = 0
        self.db.systems = {}

        self.execute_cmd("create")
        
    