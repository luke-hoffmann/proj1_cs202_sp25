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
        
        
        
        
        
            


@dataclass(frozen=True)
class Region:
    # Describes the identity and terrain of a region.
    
    rect: GlobeRect # a `GlobeRect` object describing the physical boundaries
    name: str # a string with the name of the region (e.g., `"Tokyo"`)
    terrain: str # a string representing the terrain type — one of: ocean, mountains, forest, or other
    

@dataclass(frozen=True)
class RegionCondition:
    # Describes the current state of a region in a specific year.
    
    region: Region # a `Region` object
    year: int # the year of observation (as an integer)
    pop: int # the population in that year (as an integer)
    ghg_rate: float # the greenhouse gas emissions for that year (as a float, in tons of CO₂-equivalent per year)
    
    
    
    
# Create **four instances** of `RegionCondition`. These will be used to test your functions in later tasks.

# Your list must include:
# 1. A major metropolitan area from anywhere in the world
# 2. A second major metro from a different continent
# 3. A substantial ocean region (not a whole ocean)
# 4. A region that includes Cal Poly, but excludes:
#    - San Jose
#    - Santa Barbara
#    - Bakersfield
#    - and too much ocean


major_metro_globerect = GlobeRect(40.460702,40.943033,-74.379615,-73.709381)

major_metro_region = Region(major_metro_globerect,"New York City", "other")
major_metro = RegionCondition(major_metro_region,2024,8584629,78740000)

second_major_metro_globerect = GlobeRect(18.874808,19.274153,72.711445,72.977678)
second_major_metro_region = Region(second_major_metro_globerect,"Mumbai", "other")
second_major_metro = RegionCondition(second_major_metro_region,2024,25300000,5.6e7)

south_china_sea_globerect = GlobeRect(12.061978,18.038351,117.376528,110.967700)
south_china_sea_region = Region(south_china_sea_globerect,"South China Sea", "ocean")
south_china_sea = RegionCondition(south_china_sea_region,2024,0,2.0e10)

cal_poly_globerect = GlobeRect(35.238162,35.324984,-120.609130,-120.710445,)
cal_poly_region = Region(cal_poly_globerect,"Cal Poly","mountains")
cal_poly = RegionCondition(cal_poly_region,2024,47000,4.7e5)
region_conditions = [major_metro,second_major_metro,south_china_sea,cal_poly]
# > Use rough estimates. Approximate within:
# > - ~5% for latitude/longitude  
# > - Factor of 10 for population or emissions  
# > Don’t spend more than 5–10 minutes researching numbers.


def emissions_per_capita(rc: RegionCondition)-> float:
    # Takes a `RegionCondition` and returns the tons of CO₂-equivalent **emitted per person** in the region per year. Avoid division by zero — return `0.0` if population is zero.
    # Inputs:
    #   rc: RegionCondition -> the RegionCondition that the function will evaluate
    # Outputs:
    #   float -> a float that indicates the tons of CO₂-equivalent emitted per person in the region per year
    #         -> returns 0 if the population in the region is 0
    pop: int = rc.pop
    if (pop==0): return 0.0
    return rc.ghg_rate/pop
