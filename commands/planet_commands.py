'''
Created on Aug 1, 2018

@author: imanewman
'''

from evennia import Command
from evennia import CmdSet
from random import randint

""" -------------------------------- GLOBALS -------------------------------- """

RESOURCE_MIN_CNT = 0
RESOURCE_MAX_CNT = 100

RESOURCE_RAW_TYPES = 	["Wood", "Iron", "Gold", "Silver", "Water", 
						"Oil", "Stone", "Diamond", "Glass", "Copper",
						"Helium", "Hydrogen", "Silicon"]

RESOURCE_COMPLEX_TYPES = 	["RocketFuel", "CarbonFiber", "Batteries", 
							"Conductors", "CopperWire"]

RESOURCE_MULTIPLIERS = {
	"Aquatic":{"Wood":0.0}, 
	"Frozen":{"Wood":0.0}, 
	"Oasis":{"Wood":3.0},
	"Gasious":{"Wood":0.0}, 
	"Volcanic":{"Wood":0.0}, 
	"Tech":{}
}

""" -------------------------------- COMMANDS ------------------------------- """

class PlanetCommandGenerateResources(Command):
	"""
	Generate Planet Resources

	PLANET RESOURCES
	---
	  Raw Resources: <resource name> (<resource count>), ...
	  Complex Resources: <resource name> (<resource count>), ...

	"""

	key = "generate resources"

	# randomly generates a planets resources
	def generateResources(self, planet_type):
		resources = {}

		for resourceName in (RESOURCE_COMPLEX_TYPES + RESOURCE_RAW_TYPES):
			if resourceName in RESOURCE_MULTIPLIERS[planet_type].keys():
				multiplier = RESOURCE_MULTIPLIERS[planet_type][resourceName]
			else:
				multiplier = 1

			resources[resourceName] = 
					int(multiplier * randint(RESOURCE_MIN_CNT, RESOURCE_MAX_CNT))

		return resources

	# returns a string representation of the planets resources
	def displayResources(self, resources):
		resourcesString = "\nPLANET RESOURCES\n---"

		for resourceType in [["\nRaw Resources: ", RESOURCE_RAW_TYPES], 
							["\nComplex Resources", RESOURCE_COMPLEX_TYPES]]:
			resourcesString += resourceType[0]

			onLineCnt = 0
			for resourceName in resourceType[1]:
				if onLineCnt % 4 == 3: resourcesString += "\n\t\t"
				resourcesString += resourceName + " (" + str(resources[resourceName]) + ") "
				onLineCnt += 1

		return resourcesString

	def func(self):
		caller = self.caller
		planet = self.obj

		if planet.ndb.resources == {}: # generate resources if they havent been generated yet
			planet.ndb.resources = self.generateResources()

		resourcesString = self.displayResources(planet.ndb.resources)

		caller.msg(resourcesString)

class PlanetCmdSet(CmdSet):
    key = "planetcmdset"

    def at_cmdset_creation(self):     
        self.add(PlanetCommandGenerateResources())