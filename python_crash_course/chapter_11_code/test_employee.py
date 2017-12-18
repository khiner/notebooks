import unittest
from employee import Employee

class EmployeeTest(unittest.TestCase):
    """Tests the Employee class."""

    def setUp(self):
        self.employee = Employee('Greg', 'Turkington', 100_000)

    def test_give_default_raise(self):
        previous_annual_salary = self.employee.annual_salary
        self.employee.give_raise()
        self.assertEqual(previous_annual_salary + 5_000, self.employee.annual_salary)

    def test_give_custom_raise(self):
        previous_annual_salary = self.employee.annual_salary
        self.employee.give_raise(10_000)
        self.assertEqual(previous_annual_salary + 10_000, self.employee.annual_salary)

unittest.main()
