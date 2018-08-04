

from evennia import DefaultRoom

STAR_TYPES = ["Yellow"]

class StarSystem(DefaultRoom):
    
    def at_object_creation(self):
        self.db.number = None
        self.db.star_type = None
        self.db.dsport = None
        self.db.orbits = []
        self.db.desc = "Unconfigured Star Sector"
        
    def at_object_receive(self, moved_obj, source_location, **kwargs):
        # todo: add to ports, orbits, etc
        # todo: if character, without space suit, character dies in 10 seconds
        pass