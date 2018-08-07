

from evennia import DefaultRoom
from objects import Object
from commands.star_system_commands import StarSystemCmdSet

""" --------------------------------- OBJECT -------------------------------- """

class StarSystem(DefaultRoom):
    
    def at_object_creation(self):
        self.cmdset.add(StarSystemCmdSet, permanent=True)

        self.db.number = None
        self.db.stars = []
        self.db.dsport = None
        self.db.orbits = []
        self.db.orbit_count = 0
        self.db.desc = "Unconfigured Star Sector"

        self.execute_cmd("createStarSystem")
        
    def at_object_receive(self, moved_obj, source_location, **kwargs):
        # todo: add to ports, orbits, etc
        # todo: if character, without space suit, character dies in 10 seconds
        pass