'''
Created on Aug 1, 2018

@author: imanewman
'''

from objects import Object
from commands.planet_commands import PlanetCmdSet
from random import randint

""" -------------------------------- GLOBALS -------------------------------- """

PLANET_TYPES = ["Aquatic", "Frozen", "Oasis", "Gasious", "Volcanic", "Tech"]

""" --------------------------------- OBJECT -------------------------------- """

class Planet(Object):
    def at_object_creation(self):
        self.cmdset.add(PlanetCmdSet, permanent=True)

        self.db.desc = "Planet"
        self.db.places = []
        self.getPlanetType();

        self.ndb.resources = {}

    # randomly decided planet type
    def getPlanetType(self):
    	self.db.planet_type = PLANET_TYPES[randint(0, len(PLANET_TYPES) - 1)]

    #def at_init(self): # re-called every time the object is reinitialized
    #	self.cmdset.PlanetCommandGenerateResources()
