'''
Created on Aug 1, 2018

@author: imanewman
'''

# @create/dop myPlanet:planet.Planet
# generateResources myPlanet

from objects import Object
from commands.planet_commands import PlanetCmdSet

""" --------------------------------- OBJECT -------------------------------- """

class Planet(Object):
    def at_object_creation(self):
        self.cmdset.add(PlanetCmdSet, permanent=True)

        self.db.desc = "Planet"
        self.db.number = -1
        self.db.places = []
        self.db.planet_type = ""
        self.db.planet_size = ""

        self.db.resources = {}
        
        self.execute_cmd("create")

     # generates new resources at at restart
    def at_init(self):
        self.execute_cmd("generateResources")
