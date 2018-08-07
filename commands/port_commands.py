'''
Created on Aug 1, 2018

@author: imanewman
'''

from evennia import Command
from evennia import CmdSet
from commands.planet_commands import *
from random import randrange

""" -------------------------------- GLOBALS -------------------------------- """

ITEM_PRICES = {}

""" -------------------------------- COMMANDS ------------------------------- """

class PortCommandCreate(Command):
	"""
	Create A Port
	"""

	key = "createPort"
	
	def getItemPrices(self):
		prices = {}

		for resourceType in [[RESOURCE_RAW_TYPES, 10], [RESOURCE_COMPLEX_TYPES, 100]]:
			for resource in resourceType[0]:
				mult = randrange(7, 13) * 0.1
				if resource in ITEM_PRICES.keys():
					prices[resource] = mult * ITEM_PRICES["resource"]
				else:
					prices[resource] = mult * resourceType[1]

		return prices

	def func(self):
		caller = self.caller
		port = self.obj

		port.db.prices = self.getItemPrices()

		print "Port Created"

class PortCmdSet(CmdSet):
    key = "portcmdset"

    def at_cmdset_creation(self):     
        self.add(PortCommandCreate())