'''
Created on Aug 1, 2018

@author: imanewman
'''

from evennia import Command
from evennia import CmdSet
import random

""" -------------------------------- GLOBALS -------------------------------- """

RESOURCE_MAX_CNT = 100

RESOURCE_RAW_TYPES = 	["Wood", "Iron", "Gold", "Silver", "Water", 
						"Oil", "Stone", "Diamond", "Glass", "Copper",
						"Helium", "Hydrogen", "Silicon"]

RESOURCE_COMPLEX_TYPES = 	["RocketFuel", "CarbonFiber", "Batteries", 
							"Conductors", "CopperWire"]

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
	def generateResources(self):
		resources = {}

		for resourceName in (RESOURCE_COMPLEX_TYPES + RESOURCE_RAW_TYPES):
			resources[resourceName] = random.randrange(RESOURCE_MAX_CNT)

		return resources

	# returns a string representation of the planets resources
	def displayResources(self, resources):
		resourcesString = "\nPLANET RESOURCES\n---"

		for resourceType in ["\nRaw Resources: ", "\nComplex Resources"]:
			resourcesString += resourceType

			onLineCnt = 0
			for resourceName in RESOURCE_RAW_TYPES:
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