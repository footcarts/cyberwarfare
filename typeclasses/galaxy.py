from commands.galaxy_commands import GalaxyCmdSet
from evennia import DefaultRoom

class Galaxy(DefaultRoom):
    def at_object_creation(self):
        self.db.system_count = 0
        self.db.systems = {}
        self.cmdset.add(GalaxyCmdSet, permanent=True)
        
    