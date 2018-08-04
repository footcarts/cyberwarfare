

from evennia import DefaultRoom
from objects import Object
from commands.star_system_commands import StarSystemCmdSet
from random import randint

""" -------------------------------- GLOBALS -------------------------------- """

STAR_TYPES = ["Yellow", "Brown"]

""" --------------------------------- OBJECT -------------------------------- """

class StarSystem(DefaultRoom):
    
    def at_object_creation(self):
        self.cmdset.add(StarSystemCmdSet, permanent=True)

        self.db.number = None
        self.db.star_type = None
        self.db.dsport = None
        self.db.orbits = []
        self.db.orbit_count = 0
        self.db.desc = "Unconfigured Star Sector"

        self.getStarType()
        self.execute_cmd("create")

    def getStarType(self):
        self.db.star_type = STAR_TYPES[randint(0, len(STAR_TYPES) - 1)]
        
    def at_object_receive(self, moved_obj, source_location, **kwargs):
        # todo: add to ports, orbits, etc
        # todo: if character, without space suit, character dies in 10 seconds
        pass