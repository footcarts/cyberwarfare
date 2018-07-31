
from evennia import Command
from evennia import CmdSet
from evennia import DefaultExit

from typeclasses.star_system import StarSystem
from evennia import create_object

import random

class GalaxyCommandCreate(Command):
    """
    Create a random galaxy map
    """
    key="create"
    
    def func(self):
        galaxy = self.obj
        if self.args:
            system_count, = self.args
        else:
            system_count = 50
        galaxy.db.system_count = system_count
        degrees = {}
        for i in range(system_count):
            print "creating star system %s"%(i+1)
            star_system = create_object(StarSystem, 
                                                 key="system_%s"%i,
                                                 location=galaxy)
            star_system.db.number = i+1
            star_system.db.desc = "Star System %s" % (i+1)
            galaxy.db.systems[i+1] = star_system.dbref
            
            prob = random.random()
            print "Prob", prob
            # we want degree to be 3-4 50 % of the time, 2 10%, 5-9 30%, 1 5%, 10 5%
            if prob < .5:
                degree = random.randint(2,3)
            elif prob < .60:
                degree = 2#random.randint(2,3)
            elif prob < .90:
                degree = random.randint(5,9)
            elif prob < .95:
                degree = 1
            else:
                degree = 10
            degrees[i+1] = degree
            print "Assigning %s degree to system %s" % (degree, i+1)
        
        incomplete = set(range(1,system_count+1))
        edges = [1]
        
        while edges:
            # will repeat until incomplete is empty
            # edges gets a new incomplete system every time
            # through the loop unless warps_needed is 0 and there
            # are still edges left
            
            system = edges.pop(0)
            
            print "Creating connections for star system %s with %s additional warps needed" % (system, degrees[system])
            warps_needed = degrees[system]
            
            # special case. If warps_needed is 0 and edges is empty, increase by 1
            if warps_needed == 0 and len(edges) == 0:
                print "increasing degree by 1 to prevent stagnation"
                warps_needed = 1
                
            # by the end of this function, this system will be finished
            # so set degrees remaining to 0 and remove from incomplete
            degrees[system] = 0
            
            # it's possible that system was already marked complete
            # (i.e., removed from the incomplete set) but we still
            # had to process it anyway (e.g., to prevent stagnation).
            # so use an if statement to see if it's there before removing
            if system in incomplete:
                incomplete.remove(system)
            
            # remove from incomplete before finding warps, otherwise could get
            # a connection to ourself   
            disconnected_warps = random.sample(incomplete, min(warps_needed, len(incomplete)))
            for warp in disconnected_warps:
                print "Connecting %s and %s" % (system, warp)
                self.connect(system, warp)
                degrees[warp] -= 1
                if degrees[warp] <= 0:
                    incomplete.remove(warp)
                else:
                    edges.append(warp)
            
    def connect(self, sector_n, sector_m):
        galaxy = self.obj
        warp_a = create_object(DefaultExit, "%s"%sector_n, 
                                location=galaxy.db.systems[sector_m],
                                destination=galaxy.db.systems[sector_n])
        warp_b = create_object(DefaultExit, "%s"%sector_m,
                                location=galaxy.db.systems[sector_n],
                                destination=galaxy.db.systems[sector_m])
        return (warp_a, warp_b)


class GalaxyCmdSet(CmdSet):
    """
    This allows mechs to do do mech stuff.
    """
    key = "galaxycmdset"

    def at_cmdset_creation(self):
        "Called once, when cmdset is first created"        
        self.add(GalaxyCommandCreate())