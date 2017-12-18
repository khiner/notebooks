"""User, Admin and Privilege classes."""

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

class Privileges():
    def __init__(self, privileges=['can add post', 'can delete post']):
        self.privileges = privileges

    def show(self):
        print('\nPrivileges:')
        for privilege in self.privileges:
            print('\t' + privilege)

class Admin(User):
    """Represents an admin user."""
    def __init__(self, first_name, last_name, privileges=Privileges()):
        super().__init__(first_name, last_name)
        self.privileges = privileges
