'''
Created on Aug 1, 2018

@author: imanewman
'''

# @create/dop myPlanet:planet.Planet
# generateResources myPlanet

from objects import Object
from commands.planet_commands import PlanetCmdSet
from random import randint

""" -------------------------------- GLOBALS -------------------------------- """

PLANET_TYPES = ["Aquatic", "Frozen", "Oasis", "Gasious", "Volcanic", "Tech"]

PLANET_SIZES = ["Small", "Medium", "Large", "Massive"]

""" --------------------------------- OBJECT -------------------------------- """

class Planet(Object):
    def at_object_creation(self):
        self.cmdset.add(PlanetCmdSet, permanent=True)

        self.db.desc = "Planet"
        self.db.places = []
        self.db.planet_type = None
        self.db.planet_size = None

        self.ndb.resources = {}
        
        self.getPlanetType()

    # randomly decided planet type
    def getPlanetType(self):
    	self.db.planet_type = PLANET_TYPES[randint(0, len(PLANET_TYPES) - 1)]
    	self.db.planet_size = PLANET_SIZES[randint(0, len(PLANET_SIZES) - 1)]

    # generates new resources at at restart
    def at_init(self):
    	self.execute_cmd("generateResources")