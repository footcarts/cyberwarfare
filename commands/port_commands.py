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
					prices[resource] = int(mult * ITEM_PRICES["resource"])
				else:
					prices[resource] = int(mult * resourceType[1])

		return prices

	def func(self):
		caller = self.caller
		port = self.obj

		port.db.prices = self.getItemPrices()
		port.db.sell_ratio = randrange(3, 8) * 0.1

		print "Port Created"

class PortCommandDisplay(Command):
	"""
	Display Port Items and Prices

	PORT TRADING (Sell for X% Price)
	---
	  <Item> (<Amount>):	$<Price>  |  <Item> (<Amount>):	$<Price>
	  <Item> (<Amount>):	$<Price>  |  <Item> (<Amount>):	$<Price>
	"""

	key = "display"

	def displayPrices(self, port):
		prices = port.db.prices
		sell_ratio = port.db.sell_ratio
		planet = port.db.planet
		counter = 0
		displayString = "PORT TRADING (Sell for " + str(int(sell_ratio * 100)) + "% price)\n---\n  "

		for key, value in prices.items():
			resourceCount = planet.db.resources[key]
			displayString += "  {0:>10} ({1:>4}): {2:>4}  |".format(key, str(resourceCount), str(value))
			counter += 1
			if counter % 3 == 0: displayString += "\n"

		return displayString

	def func(self): # todo: make able to display kind or one resource with args
		port = self.obj
		desc = port.db.desc
		caller = self.caller

		caller.msg(self.displayPrices(port))

		print desc + " Prices Displayed"

class PortCmdSet(CmdSet):
    key = "portcmdset"

    def at_cmdset_creation(self):     
        self.add(PortCommandCreate())
        self.add(PortCommandDisplay())