'''
Created on Aug 1, 2018

@author: imanewman
'''

from evennia import Command
from evennia import CmdSet

#class PortCommand(Command):
#	key = "command name"
#	def func(self)

class PortCmdSet(CmdSet):
    key = "portcmdset"

    def at_cmdset_creation(self):     
        #self.add(PortCommand())