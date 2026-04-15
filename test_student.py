import unittest
from proj1 import area, emissions_per_capita, emissions_per_square_km, densest, project_condition, GlobeRect, RegionCondition, Region
from math import pi,sin
class TestGlobeRect(unittest.TestCase):
    def test_typical(self):
        # test that dataclass set __str__
        gr: GlobeRect = GlobeRect(10,20,30,20)
        self.assertEqual(isinstance(gr,GlobeRect),True)
        self.assertEqual(str(gr), "GlobeRect(lo_lat=10, hi_lat=20, west_long=30, east_long=20)")
        
        # test that dataclass set __eq__
        gr2: GlobeRect = GlobeRect(10,20,30,20)
        gr3: GlobeRect = GlobeRect(10,21,31,20)
        self.assertEqual(gr,gr2)
        self.assertNotEqual(gr2,gr3)
    def test_malformed_inputs(self):
        # latitudes must be between -90 and 90
        self.assertRaises(ValueError, lambda: GlobeRect(91,92,30,20))
        self.assertRaises(ValueError, lambda: GlobeRect(-100,20,30,20))
        self.assertRaises(ValueError, lambda: GlobeRect(-192,-190,30,20))
        self.assertRaises(ValueError, lambda: GlobeRect(30,190,30,20))
        
        # longitudes must be between -180 and 180
        self.assertRaises(ValueError, lambda: GlobeRect(30,40,190,20))
        self.assertRaises(ValueError, lambda: GlobeRect(30,40,-190,20))
        self.assertRaises(ValueError, lambda: GlobeRect(30,40,30,190))
        self.assertRaises(ValueError, lambda: GlobeRect(30,40,30,-190))
        
        # hi_lat must be bigger than lo_lat
        self.assertRaises(ValueError, lambda: GlobeRect(30,20,30,20))
        
        # cannot pass str as float
        self.assertRaises(TypeError, lambda: GlobeRect("cheese",20,30,20))
        
        # cannot pass bool as float
        self.assertRaises(TypeError, lambda: GlobeRect(False,20,30,20))
        
        # cannot pass infinity as it is not finite
        self.assertRaises(ValueError, lambda: GlobeRect(float("inf"),20,30,20))
class TestEmissionsPerCapita(unittest.TestCase):
    def test_typical(self):
        # test that emissions per capita is properly calculated under normal conditions
        gc = GlobeRect(0,10,10,20)
        region = Region(gc,"China","mountains")
        rc = RegionCondition(region,2020,10000,1500)
        self.assertEqual(emissions_per_capita(rc),1500/10000)
        # test that emissions per capita is properly calculated
        rc = RegionCondition(region,2020,1567801235,150025)
        self.assertEqual(emissions_per_capita(rc),150025/1567801235)
    def test_edge_cases(self):
        # test that emissions per capita properly handles dividing by zero
        gc = GlobeRect(0,10,10,20)
        region = Region(gc,"Ocean","ocean")
        rc = RegionCondition(region,2020,0,1500)
        self.assertEqual(emissions_per_capita(rc),0)
class TestEmissionsPerSquareKm(unittest.TestCase):
    def test_typical(self):
        # test that emissions per square km is properly calculated under normal conditions
        gc = GlobeRect(0,10,10,20)
        region = Region(gc,"China","mountains")
        rc = RegionCondition(region,2020,10000,1500)
        self.assertEqual(emissions_per_square_km(rc),1500/area(rc.region.rect))
    def test_edge_cases(self):
        # test that emissions per square km properly handles dividing by zero
        gc = GlobeRect(0,0,0,0)
        region = Region(gc,"China","mountains")
        rc = RegionCondition(region,2020,10000,1500)
        self.assertEqual(emissions_per_square_km(rc),0)
        
class TestArea(unittest.TestCase):
    DEGREES_TO_RADIANS: float = pi / 180
    EARTH_RADIUS: float = 6378.1 # km
    EARTH_RADIUS_SQUARED = EARTH_RADIUS**2
    def test_typical_area(self):
        # test typical GlobeRects
        low_lat = -40
        hi_lat=40
        east_long = 5
        west_long = -6
        gr: GlobeRect = GlobeRect(low_lat,hi_lat,west_long,east_long)
        lat_term = abs(sin(hi_lat * self.DEGREES_TO_RADIANS) - sin(low_lat*self.DEGREES_TO_RADIANS))
        long_term = east_long - west_long
        if long_term <0 : long_term+= 360
        long_term = abs(long_term * self.DEGREES_TO_RADIANS)
        expected_area = lat_term * long_term * self.EARTH_RADIUS_SQUARED
        self.assertAlmostEqual(area(gr),expected_area,3)
        
        low_lat = -10
        hi_lat=1.005
        east_long = 60
        west_long = -60
        gr: GlobeRect = GlobeRect(low_lat,hi_lat,west_long,east_long)
        lat_term = abs(sin(hi_lat * self.DEGREES_TO_RADIANS) - sin(low_lat*self.DEGREES_TO_RADIANS))
        long_term = east_long - west_long
        if long_term <0 : long_term+= 360
        long_term = abs(long_term * self.DEGREES_TO_RADIANS)
        expected_area = lat_term * long_term * self.EARTH_RADIUS_SQUARED
        self.assertAlmostEqual(area(gr),expected_area,3)
        
    def test_long_across_180_line(self):
        # test a GlobeRect where the longitudes cross the 180 degree line
        low_lat = -20
        hi_lat= 40
        east_long = 170
        west_long = -170
        gr: GlobeRect = GlobeRect(low_lat,hi_lat,west_long,east_long)
        lat_term = abs(sin(hi_lat * self.DEGREES_TO_RADIANS) - sin(low_lat*self.DEGREES_TO_RADIANS))
        long_term = east_long - west_long
        if long_term < 0 : long_term+= 360
        long_term = abs(long_term * self.DEGREES_TO_RADIANS)
        expected_area = lat_term * long_term * self.EARTH_RADIUS_SQUARED
        self.assertAlmostEqual(area(gr),expected_area,3)
class TestDensest(unittest.TestCase):
    def test_typical(self):
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
        self.assertEqual(densest(region_conditions),"New York City")
    def test_edge_cases(self):
        self.assertRaises(IndexError,lambda: densest([]))
        self.assertRaises(TypeError,lambda: densest(["cheese"]))
class TestProjectCondition(unittest.TestCase):
    def test_typical(self):
        
    def test_edge_cases(self):
        self.assertRaises(IndexError,lambda: project_condition("string",10))
        self.assertRaises(ValueError, lambda: project_condition([]))
if __name__ == '__main__':
    unittest.main()
