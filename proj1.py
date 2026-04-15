#complete your tasks in this file
import sys
from dataclasses import dataclass
from math import pi, inf, sin,isfinite
from typing import Any
import numbers
sys.setrecursionlimit(10**6)
DEGREES_TO_RADIANS: float = pi / 180
EARTH_RADIUS: float = 6378.1 # km
def assertFinite(x : Any)->None:
    if not isinstance(x, numbers.Real): raise TypeError
    if isinstance(x,bool): raise TypeError
    if not isfinite(x): raise ValueError
@dataclass(frozen=True)
class GlobeRect:
    # Represents a rectangular region of the globe.
    
    lo_lat: float # the lower latitude in degrees 
    hi_lat:float # the upper latitude in degrees 
    west_long:float # the western longitude in degrees
    east_long:float # the eastern longitude in degrees
    def __post_init__(self):
        # forces lo_lat < hi_lat and west_long < east_long
        assertFinite(self.lo_lat)
        assertFinite(self.hi_lat)
        assertFinite(self.west_long)
        assertFinite(self.east_long)
        error_message = ""
        if abs(self.lo_lat) >90: error_message+=("lo_lat must be between -90 and 90")
        if abs(self.hi_lat) >90: error_message+=("hi_lat must be between -90 and 90")
        if abs(self.west_long) >180: error_message+=("west_long must be between -180 and 180")
        if abs(self.east_long) >180: error_message+=("east_long must be between -180 and 180")
        if self.lo_lat > self.hi_lat: error_message+=("the lower latitude is higher that the upper latitude")
        if (len(error_message) > 0): raise ValueError(error_message)
        
        
        
        
        
            


