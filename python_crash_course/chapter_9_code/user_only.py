"""User class only."""

class User():
    """Represents a forum user."""
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.login_attempts = 0
    
    def describe_user(self):
        print('User summary:')
        print('\tFirst name: ' + self.first_name.title())
        print('\tLast name: ' + self.last_name.title())

    def greet_user(self):
        print('Hello ' + self.first_name.title() + '!')
        
    def increment_login_attempts(self):
        self.login_attempts += 1
    
    def reset_login_attempts(self):
        self.login_attempts = 0
