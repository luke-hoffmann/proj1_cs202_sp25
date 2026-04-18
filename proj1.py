#complete your tasks in this file
import sys
from dataclasses import dataclass
from math import pi, inf, sin,isfinite
from typing import Any, Self, Literal

import numbers
sys.setrecursionlimit(10**6)
DEGREES_TO_RADIANS: float = pi / 180
EARTH_RADIUS: float = 6378.1 # km
def assertFiniteFloat(x : Any)->None:
    # Verifies that x is a finite float-like numeric value.
    # Inputs:
    #   x: Any -> the value to validate as a finite float-like number
    # Outputs:
    #   None -> returns nothing if x is valid
    # Preconditions:
    #   x should be intended to represent a numeric value
    # Postconditions:
    #   the function either finishes with no return value or raises an error
    # Examples:
    #   assertFiniteFloat(3.5) returns None
    #   assertFiniteFloat(float("inf")) raises ValueError
    if not isinstance(x, numbers.Real): raise TypeError
    if isinstance(x,bool): raise TypeError
    if not isfinite(x): raise ValueError
def assertFiniteInt(x: Any)->None:
    # Verifies that x is a finite integer value.
    # Inputs:
    #   x: Any -> the value to validate as a finite integer
    # Outputs:
    #   None -> returns nothing if x is valid
    # Preconditions:
    #   x should be intended to represent an integer value
    # Postconditions:
    #   the function either finishes with no return value or raises an error
    # Examples:
    #   assertFiniteInt(5) returns None
    #   assertFiniteInt(5.2) raises TypeError
    if not isinstance(x, numbers.Real): raise TypeError
    if isinstance(x,bool): raise TypeError
    if not isfinite(x): raise ValueError
    if not isinstance(x,int): raise TypeError
@dataclass(frozen=True)
class GlobeRect:
    # Represents a rectangular region of the globe.
    
    lo_lat: float # the lower latitude in degrees 
    hi_lat:float # the upper latitude in degrees 
    west_long:float # the western longitude in degrees
    east_long:float # the eastern longitude in degrees
    def __post_init__(self):
        # forces lo_lat < hi_lat and west_long < east_long
        # Inputs:
        #   self: GlobeRect -> the GlobeRect being validated after construction
        # Outputs:
        #   None -> returns nothing if all fields are valid
        # Preconditions:
        #   the dataclass fields have already been assigned
        # Postconditions:
        #   this GlobeRect has finite coordinates in valid latitude/longitude ranges
        # Examples:
        #   GlobeRect(10,20,30,40) passes validation
        #   GlobeRect(95,20,30,40) raises ValueError
        assertFiniteFloat(self.lo_lat)
        assertFiniteFloat(self.hi_lat)
        assertFiniteFloat(self.west_long)
        assertFiniteFloat(self.east_long)
        error_message = ""
        if abs(self.lo_lat) >90: error_message+=("lo_lat must be between -90 and 90")
        if abs(self.hi_lat) >90: error_message+=("hi_lat must be between -90 and 90")
        if abs(self.west_long) >180: error_message+=("west_long must be between -180 and 180")
        if abs(self.east_long) >180: error_message+=("east_long must be between -180 and 180")
        if self.lo_lat > self.hi_lat: error_message+=("the lower latitude is higher that the upper latitude")
        if (len(error_message) > 0): raise ValueError(error_message)
    def copy(self)->Self:
        # Creates an identical GlobeRect.
        # Inputs:
        #   self: GlobeRect -> the GlobeRect to copy
        # Outputs:
        #   Self -> a new GlobeRect with the same coordinate values
        # Preconditions:
        #   self is a valid GlobeRect
        # Postconditions:
        #   the returned GlobeRect is equal to self
        # Examples:
        #   GlobeRect(10,20,30,40).copy() returns GlobeRect(10,20,30,40)
        return type(self)(self.lo_lat,self.hi_lat,self.west_long,self.east_long)
        
@dataclass(frozen=True)
class Region:
    # Describes the identity and terrain of a region.
    
    rect: GlobeRect # a `GlobeRect` object describing the physical boundaries
    name: str # a string with the name of the region (e.g., `"Tokyo"`)
    terrain: str # a string representing the terrain type — one of: ocean, mountains, forest, or other
    def __post_init__(self):
        # Validates the contents of a Region after construction.
        # Inputs:
        #   self: Region -> the Region being validated after construction
        # Outputs:
        #   None -> returns nothing if all fields are valid
        # Preconditions:
        #   the dataclass fields have already been assigned
        # Postconditions:
        #   this Region has a GlobeRect, a string name, and an allowed terrain
        # Examples:
        #   Region(GlobeRect(0,10,10,20),"Tokyo","other") passes validation
        #   Region(GlobeRect(0,10,10,20),"Tokyo","desert") raises ValueError
        allowableTerrains = {"mountains","ocean","forest","other"}
        if not self.terrain in allowableTerrains: raise ValueError
        if not isinstance(self.name,str): raise TypeError
        if not isinstance(self.rect,GlobeRect): raise TypeError
        if not isinstance(self.terrain,str): raise TypeError
    def copy(self)->Self:
        # Creates an identical Region.
        # Inputs:
        #   self: Region -> the Region to copy
        # Outputs:
        #   Self -> a new Region with the same field values
        # Preconditions:
        #   self is a valid Region
        # Postconditions:
        #   the returned Region is equal to self
        # Examples:
        #   Region(GlobeRect(0,10,10,20),"Tokyo","other").copy() returns an equal Region
        return type(self)(self.rect.copy(),self.name,self.terrain)
@dataclass(frozen=True)
class RegionCondition:
    # Describes the current state of a region in a specific year.
    
    region: Region # a `Region` object
    year: int # the year of observation (as an integer)
    pop: int # the population in that year (as an integer)
    ghg_rate: float # the greenhouse gas emissions for that year (as a float, in tons of CO₂-equivalent per year)
    def __post_init__(self):
        # Validates the contents of a RegionCondition after construction.
        # Inputs:
        #   self: RegionCondition -> the RegionCondition being validated after construction
        # Outputs:
        #   None -> returns nothing if all fields are valid
        # Preconditions:
        #   the dataclass fields have already been assigned
        # Postconditions:
        #   this RegionCondition has a Region, integer year/pop, and finite ghg_rate
        # Examples:
        #   RegionCondition(Region(GlobeRect(0,10,10,20),"A","other"),2024,100,50.0) passes validation
        #   RegionCondition(Region(GlobeRect(0,10,10,20),"A","other"),2024,1.5,50.0) raises TypeError
        if not isinstance(self.region,Region): raise TypeError
        assertFiniteInt(self.year)
        assertFiniteInt(self.pop)
        assertFiniteFloat(self.ghg_rate)
    def copy(self)->Self:
        # Creates an identical RegionCondition.
        # Inputs:
        #   self: RegionCondition -> the RegionCondition to copy
        # Outputs:
        #   Self -> a new RegionCondition with the same field values
        # Preconditions:
        #   self is a valid RegionCondition
        # Postconditions:
        #   the returned RegionCondition is equal to self
        # Examples:
        #   RegionCondition(Region(GlobeRect(0,10,10,20),"A","other"),2024,100,50.0).copy() returns an equal RegionCondition
        return type(self)(self.region.copy(),self.year,self.pop,self.ghg_rate)
    
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

south_china_sea_globerect = GlobeRect(12.061978,18.038351,110.967700,117.376528)
south_china_sea_region = Region(south_china_sea_globerect,"South China Sea", "ocean")
south_china_sea = RegionCondition(south_china_sea_region,2024,0,2.0e10)

cal_poly_globerect = GlobeRect(35.238162,35.324984,-120.710445,-120.609130)
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
    # Preconditions:
    #   rc must be a RegionCondition
    # Postconditions:
    #   returns 0.0 when rc.pop is 0, otherwise returns rc.ghg_rate / rc.pop
    # Examples:
    #   emissions_per_capita(RegionCondition(Region(GlobeRect(0,10,10,20),"A","other"),2024,100,50.0)) returns 0.5
    #   emissions_per_capita(RegionCondition(Region(GlobeRect(0,10,10,20),"A","other"),2024,0,50.0)) returns 0.0
    if not isinstance(rc,RegionCondition): raise TypeError
    pop: int = rc.pop
    if (pop==0): return 0.0
    return rc.ghg_rate/pop

def area(gr: GlobeRect)-> float:
    # Calculate the estimated surface area of the region in square kilometers.
    # Inputs:
    #   gr: GlobeRect -> the GlobeRectangle that the function will use to calculate the square kilometers
    # Outputs:
    #   float -> a float that is equivalent to the number of square kilometers inside of the GlobeRect that was passed as an input
    # Preconditions:
    #   gr must be a GlobeRect with valid latitude and longitude values
    # Postconditions:
    #   returns the spherical surface area in square kilometers for gr
    # Examples:
    #   area(GlobeRect(0,10,10,20)) returns a positive float
    #   area(GlobeRect(40,40,-6,5)) returns 0.0
    
    if not isinstance(gr, GlobeRect): raise TypeError
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
    # Preconditions:
    #   rc must be a RegionCondition
    # Postconditions:
    #   returns 0 when the region area is 0, otherwise returns rc.ghg_rate / area(rc.region.rect)
    # Examples:
    #   emissions_per_square_km(RegionCondition(Region(GlobeRect(0,10,10,20),"A","other"),2024,100,50.0)) returns 50.0 / area(GlobeRect(0,10,10,20))
    #   emissions_per_square_km(RegionCondition(Region(GlobeRect(0,0,10,20),"A","other"),2024,100,50.0)) returns 0
    if not isinstance(rc,RegionCondition): raise TypeError
    a = area(rc.region.rect)
    if (a == 0): return 0
    return rc.ghg_rate / a
def densest(rc_list : list[RegionCondition])->str:
    # Takes a list of RegionConditions and returns the name of the region with the highest population density.
    # Inputs:
    #   rc_list: list[RegionCondition] -> a list of Region Conditions to be evaluated for the highest population density
    # Outputs:
    #   str -> the name of the Region with the highest population density.
    # Preconditions:
    #   rc_list must be a non-empty list of RegionCondition values
    # Postconditions:
    #   returns the name of the RegionCondition with the greatest population divided by area
    # Examples:
    #   densest([cal_poly]) returns "Cal Poly"
    #   densest([]) raises IndexError
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
    # Preconditions:
    #   rc_list must be a list, highest_density must represent the best density seen so far, and index must be the current position being checked
    # Postconditions:
    #   returns the index of the densest RegionCondition in rc_list
    # Examples:
    #   densest_recursive([cal_poly], -inf, 0, 0) returns 0
    #   densest_recursive(region_conditions, -inf, 0, 0) returns the index of the densest region
    if (index >= len(rc_list)): 
        return highest_density_index
    if (not isinstance(rc_list[index],RegionCondition)): raise TypeError
    if (len(rc_list) ==0): raise IndexError
    A = area(rc_list[index].region.rect)
    if A == 0: 
        current_density = 0.0
    else:
        current_density = rc_list[index].pop / A
    if (current_density > highest_density): 
        highest_density = current_density
        highest_density_index = index
    return densest_recursive(rc_list,highest_density,highest_density_index,index+1)


terrain_to_growth_rate_map: dict[str,float] = {}
terrain_to_growth_rate_map["ocean"] = 0.0001
terrain_to_growth_rate_map["mountains"] = 0.0005
terrain_to_growth_rate_map["forest"] = -0.00001
terrain_to_growth_rate_map["other"] = 0.0003
def project_condition(rc : RegionCondition, years: int)->RegionCondition:
    # Projects a RegionCondition forward by a certain number of years using terrain-based growth.
    # Inputs:
    #   rc: RegionCondition -> the starting RegionCondition to project forward
    #   years: int -> the number of years to project into the future
    # Outputs:
    #   RegionCondition -> a new projected RegionCondition after the requested number of years
    # Preconditions:
    #   rc must be a RegionCondition and years must be an integer greater than or equal to 0
    # Postconditions:
    #   returns a new RegionCondition with the same region, updated year, updated population, and proportionally updated ghg_rate
    # Examples:
    #   project_condition(cal_poly,0) returns a RegionCondition equal to cal_poly
    #   project_condition(cal_poly,10) returns a RegionCondition with year 10 years later
    if years <0: raise ValueError
    if not isinstance(rc,RegionCondition): raise TypeError
    if not isinstance(years,int): raise TypeError
    growth_multiplier = growth(terrain_to_growth_rate_map,rc.region.terrain,years)
    pop = int(rc.pop * growth_multiplier)
    if pop <0: pop = 0
    ghg = rc.ghg_rate * growth_multiplier
    return RegionCondition(rc.region.copy(),rc.year+years,pop,ghg)

def growth(growth_rate_map: dict[str,float], terrain: str, years: int)->float:
    # Computes the compounded population/emissions multiplier for a terrain over a number of years.
    # Inputs:
    #   growth_rate_map: dict[str,float] -> maps each terrain to its annual growth rate
    #   terrain: str -> the terrain whose growth rate will be used
    #   years: int -> the number of years of compounding
    # Outputs:
    #   float -> the compounded growth multiplier for the given terrain and years
    # Preconditions:
    #   growth_rate_map must be a dictionary, terrain must be a key in the map, and years must be a finite integer
    # Postconditions:
    #   returns (1+growth_rate_map[terrain]) ** years
    # Examples:
    #   growth(terrain_to_growth_rate_map,"mountains",0) returns 1.0
    #   growth(terrain_to_growth_rate_map,"other",10) returns a positive float
    if not isinstance(growth_rate_map,dict): raise TypeError
    if not isinstance(terrain,str): raise TypeError
    assertFiniteInt(years)
    if not terrain in growth_rate_map: raise KeyError
    growth_rate = growth_rate_map[terrain]
    return (1+growth_rate) ** years
