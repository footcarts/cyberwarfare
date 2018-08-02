'''
Created on Aug 1, 2018

@author: imanewman
'''

from objects import Object
from commands.planet_commands import PlanetCmdSet

class Planet(Object): # should be Room?
    def at_object_creation(self):
        self.cmdset.add(PlanetCmdSet, permanent=True)

        self.db.desc = "Planet"
        self.ndb.resources = {}

    #def at_init(self): # recalled every time the object is reinitialized
    #	self.cmdset.PlanetCommandGenerateResources()