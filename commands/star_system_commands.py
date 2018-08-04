'''
Created on Aug 1, 2018

@author: imanewman
'''

from evennia import Command
from evennia import CmdSet
from random import randint
from evennia import create_object
from typeclasses.planet import Planet

""" -------------------------------- GLOBALS -------------------------------- """

PLANET_MIN_CNT = 1
PLANET_MAX_CNT = 10

""" -------------------------------- COMMANDS ------------------------------- """

class StarSystemCommandCreate(Command):
	"""
	Create Star System
	"""

	key = "create"

	def createPlanets(self, star_system):
		planets = []
		count = randint(PLANET_MIN_CNT, PLANET_MAX_CNT)

		for i in range(count):
			planet = create_object(Planet, key = "planet_%s"%i, location = star_system)

			planet.db.number = i
			planet.db.desc = planet.db.planet_size + ' ' + planet.db.planet_type 
			planet.db.desc += " Planet %s"%i

			planets.append(planet)

		return planets

	def func(self):
		caller = self.caller
		star_system = self.obj

		planets = self.createPlanets(star_system)

		star_system.db.orbits = planets
		star_system.db.orbit_count = len(planets)

		caller.msg("Star System Created")

class StarSystemCmdSet(CmdSet):
    key = "starsystemcmdset"

    def at_cmdset_creation(self):     
        self.add(StarSystemCommandCreate())