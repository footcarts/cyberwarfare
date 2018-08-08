'''
Created on Jul 18, 2018

@author: seth_
'''

from objects import Object
from commands.starship_commands import StarshipCmdSet

class Starship(Object):
    def at_object_creation(self):
        self.cmdset.add(StarshipCmdSet, permanent=True)

        self.db.desc = "Starship"
        self.db.inventory = {}