"""A class that can be used to represent restaurants."""

class Restaurant():
    """A simple model of a restaurant."""

    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type
        self.number_served = 0

    def describe_restaurant(self):
        print('Restaurant name: ' + self.restaurant_name.title())
        print('Cuisine type: ' + self.cuisine_type)
    
    def open_restaurant(self):
        print(self.restaurant_name.title() + ' is open!')
    
    def set_number_served(self, number_served):
        self.number_served = number_served
        
    def increment_number_served(self, number_new_customers):
        if number_new_customers > 0:
            self.number_served += number_new_customers
