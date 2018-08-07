'''
Created on Aug 1, 2018

@author: imanewman
'''

from evennia import Command
from evennia import CmdSet
from random import randint
from evennia import create_object
from typeclasses.planet import Planet
from typeclasses.port import Port
from random import randint

""" -------------------------------- GLOBALS -------------------------------- """

PLANET_MIN_CNT = 1
PLANET_MAX_CNT = 10

STAR_TYPES = ["Yellow", "Brown Dwarf", "Red Dwarf"]

""" -------------------------------- COMMANDS ------------------------------- """

class StarSystemCommandCreate(Command):
	"""
	Create Star System
	"""

	key = "createStarSystem"

	def getStarType(self):
		return STAR_TYPES[randint(0, len(STAR_TYPES) - 1)]

	def createOrbits(self, star_system):
		orbits = []
		count = randint(PLANET_MIN_CNT, PLANET_MAX_CNT)

		for i in range(count):
			planet = create_object(Planet, key = "planet_%s"%i, location = star_system)
			port = create_object(Port, key = "port_%s"%i, location = star_system)

			#planet.execute_cmd("createPlanet")
			planet.db.number = i
			planet.db.desc = planet.db.planet_size + ' ' + planet.db.planet_type 
			planet.db.desc += " Planet %s"%i
			planet.db.port = port.dbref

			#port.execute_cmd("createPort")
			port.db.number = i
			port.db.desc = planet.db.desc + "'s Port"
			port.db.planet = planet.dbref

			orbits.append({ "planet":planet.dbref, "port":port.dbref })

		return orbits

	def func(self):
		caller = self.caller
		star_system = self.obj

		star_system.db.star_type = self.getStarType()

		orbits = self.createOrbits(star_system)
		star_system.db.orbits = orbits
		star_system.db.orbit_count = len(orbits)

		caller.msg("Star System Created")

class StarSystemCmdSet(CmdSet):
    key = "starsystemcmdset"

    def at_cmdset_creation(self):     
        self.add(StarSystemCommandCreate())