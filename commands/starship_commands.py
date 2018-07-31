'''
Created on Jul 18, 2018

@author: seth_
'''

from evennia import Command
from evennia import CmdSet

class StarShipCommandScan(Command):
    """
    Scan a sector. Should look something like this:
    
    SYSTEM SCAN
    ---
      System system name [123] (owner, disputed, unclaimed)
      Deep Space Port port name (owner)
      Planets:
        Name-I (Type, Owner, Port)
        Asteroid Belt alpha (Type, Owner, port)
        Name-II "Planet Name" (Type, Owner, Port)
      Local Conditions:
        n <type of artificial mobile object>
        m frequencies in use
      Warp-outs: n, m, q
      
    Scan Dock (when in dock)
    Scan Planet (when on planet)
    """
    key="scan"
    
    
    def getFeatures(self, sector):
        name = sector.name
        try:
            sectorPrefix, sectorNumber = name.split("_")
            if sectorPrefix.lower() != "sector": return None
            sectorNumber = int(sectorNumber)
        except:
            return None
        warps = [int(exit.destination.name.split('_')[1]) for exit in sector.exits if exit.destination.name.lower().startswith('sector')]
        naventry = None
        docks = []
        planets = []
        beacons = []
        ships = []
        return (sectorNumber, naventry, docks, planets, beacons, warps, ships)
    
    def buildScan(self, number, naventry, docks, planets, beacons, warps, ships):
        desc = "\nSECTOR SCAN REPORT\n"
        desc += "  Star Sector %s\n" % number
        if naventry: desc += "  Sector DB: " + naventry + "\n"
        # TODO: Beacons
        if docks: desc += "  Star Docks: " + ",".join(docks) + "\n"
        if planets: desc += "  Planets: " + ",".join(planets) + "\n"
        if warps: desc += "  Jumps to sectors " + ",".join([str(w) for w in warps]) + "\n"
        # TODO ships
        return desc
        
    
    def func(self):
        location=self.obj.location
        caller = self.caller
        if not self.args:
            features = self.getFeatures(location)
            if not features:
                caller.msg("Game Error. Cannot process this location as a sector.")
            else:
                caller.msg(self.buildScan(*features))
        else:
            caller.msg("No long Range Scanners Aboard!")
			
			
class StarshipCmdSet(CmdSet):
    """
    This allows mechs to do do mech stuff.
    """
    key = "starshipcmdset"

    def at_cmdset_creation(self):
        "Called once, when cmdset is first created"        
        self.add(StarShipCommandScan())