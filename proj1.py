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

def area(gr: GlobeRect)-> float:
    # Calculate the estimated surface area of the region in square kilometers.
    # Inputs:
    #   gr: GlobeRect -> the GlobeRectangle that the function will use to calculate the square kilometers
    # Outputs:
    #   float -> a float that is equivalent to the number of square kilometers inside of the GlobeRect that was passed as an input
    
    
    long_term: float =  gr.east_long - gr.west_long
    lat_term: float = abs(sin(gr.hi_lat * DEGREES_TO_RADIANS) - sin(gr.lo_lat * DEGREES_TO_RADIANS))
    if (long_term < 0): long_term += 360
    long_term = abs(long_term*DEGREES_TO_RADIANS)
    
    return (EARTH_RADIUS**2) * long_term  * lat_term

def emissions_per_square_km(rc: RegionCondition)->float:
    # Takes a `RegionCondition` and returns the tons of CO₂-equivalent per square kilometer.
    # Inputs:
    #   rc: RegionCondition -> the RegionCondition used to calculate the number of tons of CO2 per square kilometer
    # Outputs:
    #   float -> a float equivalent to the number of tons of CO2 equivalent released per square kilometer in the given RegionCondition 
    a = area(rc.region.rect)
    if (a == 0): return 0
    return rc.ghg_rate / a
def densest(rc_list : list[RegionCondition])->str:
    # Takes a list of RegionConditions and returns the name of the region with the highest population density.
    # Inputs:
    #   rc_list: list[RegionCondition] -> a list of Region Conditions to be evaluated for the highest population density
    # Outputs:
    #   str -> the name of the Region with the highest population density.
    if (len(rc_list) ==0): raise IndexError
    return rc_list[densest_recursive(rc_list, -inf, 0, 0)].region.name
def densest_recursive(rc_list: list[RegionCondition], highest_density : float,highest_density_index: int, index : int)-> int:
    # Evaluates a list of RegionConditions to find which RegionCondition has the highest population density. Takes a list of RegionConditions, the current densest_density, the index of the Region Condition with the highest density, and the current index of the list to compare the highest density to.
    # Inputs:
    #   rc_list: list[RegionCondition] -> the list of   RegionConditions to find the highest population density from
    #   highest_density: float -> the current highest population density found in the list up to index-1
    #   highest_density_index: int -> the index of the current RegionCondition with the highest population density up until index-1
    #   index: int -> the index of the element in rc_list that will be compared against the highest_density to see if this element actually has the highest population density
    # Outputs:
    #   int -> the index of the RegionCondition in rc_list that has the highest population density
    if (index >= len(rc_list)): 
        return highest_density_index
    if (not isinstance(rc_list[index],RegionCondition)): raise TypeError
    if (len(rc_list) ==0): raise IndexError
    current_density = rc_list[index].pop / emissions_per_square_km(rc_list[index])
    if (current_density > highest_density): 
        highest_density = current_density
    return densest_recursive(rc_list,highest_density,highest_density_index,index+1)

def project_condition(rc : RegionCondition, years: int):
    pass