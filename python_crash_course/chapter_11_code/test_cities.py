import unittest
from city_functions import format_city_and_country

class CityFunctionsTestCase(unittest.TestCase):
    """Tests for 'city_functions.py'."""

    def test_city_country(self):
        formatted_city_and_country = format_city_and_country('santiago', 'chile')
        self.assertEqual(formatted_city_and_country, 'Santiago, Chile')

    def test_city_country_population(self):
        formatted_city_and_country = format_city_and_country('santiago', 'chile', 5000000)
        self.assertEqual(formatted_city_and_country, 'Santiago, Chile - population 5000000')

unittest.main()
