"""Admin and Privilege classes."""

from chapter_9_code.user_only import User

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
