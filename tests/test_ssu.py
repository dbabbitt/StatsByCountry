
#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# cd C:\Users\daveb\OneDrive\Documents\GitHub\StatsByCountry\tests
# cls
# python -m unittest test_ssu.TestSsuMethods.test_parse_to_decimal

import unittest

class TestSsuMethods(unittest.TestCase):
    
    def setUp(self):
        # Import or define parse_to_decimal and centroids_dict in your test setup
        self.parse_to_decimal = parse_to_decimal  # replace with actual import if needed
        self.centroids_dict = {
            'Akrotiri': "34 37 N, 32 58 E",
            'American Samoa': "14 20 S, 170 00 W"
        }
    
    def test_parse_to_decimal(self):
        coord1 = self.centroids_dict['Akrotiri']
        coord2 = self.centroids_dict['American Samoa']
        
        # Expected results
        expected_coord1 = (34.61666666666667, 32.96666666666667)
        expected_coord2 = (-14.333333333333334, -170.0)
        
        # Run parse_to_decimal and compare results
        self.assertAlmostEqual(self.parse_to_decimal(coord1)[0], expected_coord1[0], places=5)
        self.assertAlmostEqual(self.parse_to_decimal(coord1)[1], expected_coord1[1], places=5)
        self.assertAlmostEqual(self.parse_to_decimal(coord2)[0], expected_coord2[0], places=5)
        self.assertAlmostEqual(self.parse_to_decimal(coord2)[1], expected_coord2[1], places=5)

if __name__ == '__main__':
    unittest.main()