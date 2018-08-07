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
from math import ceil

""" -------------------------------- GLOBALS -------------------------------- """

PLANET_MIN_CNT = 1
PLANET_MAX_CNT = 10

STAR_TYPES = ["Yellow Dwarf", "Brown Dwarf", "Red Dwarf", "White Dwarf",
			"Red Giant", "Blue Giant", "Supergiant", "Neutron"]

""" -------------------------------- COMMANDS ------------------------------- """

class StarSystemCommandCreate(Command):
	"""
	Create Star System
	"""

	key = "createStarSystem"

	def getStarType(self):
		stars = []
		cnt = int(ceil(randint(1, 7) / 5.0))
		
		for i in range(cnt):
			stars.append(STAR_TYPES[randint(0, len(STAR_TYPES) - 1)])

		return stars

	def createOrbits(self, star_system):
		orbits = []
		count = randint(PLANET_MIN_CNT, PLANET_MAX_CNT)

		for i in range(count):
			planet = create_object(Planet, key = "planet_%s"%i, location = star_system)
			port = create_object(Port, key = "port_%s"%i, location = star_system)

			planet.db.number = i
			planet.db.desc = planet.db.planet_size + ' ' + planet.db.planet_type 
			planet.db.desc += " Planet %s"%i
			planet.db.port = port.dbref

			port.db.number = i
			port.db.desc = planet.db.desc + "'s Port"
			port.db.planet = planet.dbref

			orbits.append({ "planet":planet.dbref, "port":port.dbref })

		return orbits

	def func(self):
		caller = self.caller
		star_system = self.obj

		star_system.db.stars = self.getStarType()

		orbits = self.createOrbits(star_system)
		star_system.db.orbits = orbits
		star_system.db.orbit_count = len(orbits)

		print "Star System Created: " 
		print str(len(star_system.db.stars)) + " Stars"
		print str(len(orbits)) + " Orbits"

		caller.msg("Star System Created")

class StarSystemCmdSet(CmdSet):
    key = "starsystemcmdset"

    def at_cmdset_creation(self):     
        self.add(StarSystemCommandCreate())