'''
Created on Aug 1, 2018

@author: imanewman
'''

from evennia import Command
from evennia import CmdSet
from random import randint, random

""" -------------------------------- GLOBALS -------------------------------- """

PLANET_TYPES = { "Aquatic": 0.2, 
                "Frozen": 0.15, 
                "Oasis": 0.2, 
                "Gasious": 0.15, 
                "Volcanic": 0.2, 
                "Tech": 0.1 }

PLANET_SIZES = {"Small": 0.25, "Medium": 0.35, "Large": 0.25, "Massive": 0.15}

RESOURCE_MIN_CNT = 0
RESOURCE_MAX_CNT = 100

RESOURCE_RAW_TYPES = 	["Wood", "Iron", "Gold", "Silver", "Water", 
						"Oil", "Stone", "Diamond", "Glass", "Copper",
						"Helium", "Hydrogen", "Silicon", "Plutonium",
						"Steel"]

RESOURCE_COMPLEX_TYPES = 	["RocketFuel", "CarbonFiber", "Batteries", 
							"Conductors", "CopperWire"]

RESOURCE_MULT_TYPE = {
	"Aquatic":
		{ "Wood":0.0, "Water":5.0, "Glass":1.5, "CarbonFiber":0.2, 
		"Batteries":0.2, "Conductors":0.2, "CopperWire":0.5 }, 
	"Frozen":
		{ "Wood":0.0, "Water":2.0 }, 
	"Oasis":
		{ "Wood":3.0, "Diamond":1.5, "Oil":3.0 },
	"Gasious":
		{ "Wood":0.0, "Helium":2.0, "Hydrogen":2.0 }, 
	"Volcanic":
		{ "Wood":0.0, "Silicon":2.0 }, 
	"Tech":
		{ "Iron":2.0, "Steel":3.0, "RocketFuel":4.0, "CarbonFiber":2.0, 
		"Batteries":3.0, "Conductors":2.0, "CopperWire":3.0, 
		"Plutonium":2.0, "Glass":2.0, "Oil":2.0, "Copper":2.0 } }

RESOURCE_MULT_SIZE = {
	"Small":0.5,
	"Medium":1,
	"Large":1.5,
	"Massive":2 }

""" -------------------------------- COMMANDS ------------------------------- """

class PlanetCommandCreate(Command):
	"""
	Create Planet
	"""

	key = "createPlanet"

	# randomly decided planet type
	def getPlanetType(self):
		randType = random()
		accType = 0

		for key, value in PLANET_TYPES.items():
			accType += value
			if randType < accType: 
				return key
		return "Oasis" # default if somehow not set

	# randomly decided planet size
	def getPlanetSize(self):
		randSize = random()
		accSize = 0

		for key, value in PLANET_SIZES.items():
			accSize += value
			if randSize < accSize: 
				return key
		return "Medium" # default if somehow not set

	def func(self):
		caller = self.caller
		planet = self.obj

		planet.db.planet_size = self.getPlanetSize()
		planet.db.planet_type = self.getPlanetType()

		planet.execute_cmd("generate")


		print "Planet Created"

class PlanetCommandGenerateResources(Command):
	"""
	Generate Planet Resources

	PLANET RESOURCES
	---
	  Planet Type: <planet type> (<planet size>)
	  Raw Resources: <resource name> (<resource count>), ...
	  Complex Resources: <resource name> (<resource count>), ...

	"""

	key = "generate"

	# randomly generates a planets resources
	def generateResources(self, desc, planet_type, planet_size):
		resources = {}

		print "Generating " + desc + " Resources"

		for resourceName in (RESOURCE_COMPLEX_TYPES + RESOURCE_RAW_TYPES):
			if resourceName in RESOURCE_MULT_TYPE[planet_type].keys():
				multiplier = RESOURCE_MULT_TYPE[planet_type][resourceName]
				multiplier *= RESOURCE_MULT_SIZE[planet_size]
			else:
				multiplier = RESOURCE_MULT_SIZE[planet_size]

			resources[resourceName] = int(multiplier * randint(RESOURCE_MIN_CNT, RESOURCE_MAX_CNT))

		return resources

	def func(self):
		caller = self.caller
		planet = self.obj
		planet_type = planet.db.planet_type
		planet_size = planet.db.planet_size
		desc = planet.db.desc

		#if planet.ndb.resources == {}: # generate resources if they havent been generated yet
		planet.db.resources = self.generateResources(desc, planet_type, planet_size)

		print desc + " Resources Generated"

class PlanetCommandLookResources(Command):
	"""
	Look at Planet Resources

	PLANET RESOURCES
	---
	  Planet Type: <planet type> (<planet size>)
	  Raw Resources: <resource name> (<resource count>), ...
	  Complex Resources: <resource name> (<resource count>), ...

	"""

	key = "resources"

	# returns a string representation of the planets resources
	def displayResources(self, resources, planet_type, planet_size):
		resourcesString = "\nPLANET RESOURCES\n---"
		resourcesString += "\n  Planet Type: " + planet_type + " (" + planet_size + ')'

		for resourceType in [["\n  Raw Resources: ", RESOURCE_RAW_TYPES], 
							["\n  Complex Resources: ", RESOURCE_COMPLEX_TYPES]]:
			resourcesString += resourceType[0]

			onLineCnt = 0
			for resourceName in resourceType[1]:
				if onLineCnt % 4 == 3: resourcesString += "\n    "
				try: 
					resourcesString += resourceName + " (" + str(resources[resourceName]) + ") "
					onLineCnt += 1
				except: pass

		return resourcesString

	def func(self):
		caller = self.caller
		planet = self.obj
		planet_type = planet.db.planet_type
		planet_size = planet.db.planet_size
		resources = planet.db.resources

		resourcesString = self.displayResources(resources, planet_type, planet_size)

		caller.msg(resourcesString)

class PlanetCmdSet(CmdSet):
    key = "planetcmdset"

    def at_cmdset_creation(self):     
        self.add(PlanetCommandCreate())
        self.add(PlanetCommandGenerateResources())
        self.add(PlanetCommandLookResources())