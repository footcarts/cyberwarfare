'''
Created on Aug 1, 2018

@author: imanewman
'''

from objects import Object
from commands.port_commands import PortCmdSet

class Port(Object):
    def at_object_creation(self):
        self.cmdset.add(PortCmdSet, permanent=True)

        self.db.desc = "Port"
        self.db.orbiting_planet = None