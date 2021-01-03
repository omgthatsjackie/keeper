from sys import exit
from getpass import getpass
from utils.decorators import logged

class Commands:
    def __init__(self, database):
        self.commands_list = {
            'help': {
                'description': 'print all available commands',
                'action': self.__help
            },
            'login': {
                'description': 'login to Keeper',
                'action': self.login
            },
            'logout': {
                'description': 'logout of Keeper',
                'action': self.logout
            },
            'register': {
                'description': 'register on Keeper',
                'action': self.register
            },
            'exit': {
                'description': 'exit Keeper',
                'action': self.exit
            },
            'store': {
                'description': 'store credentials of a particular app',
                'action': self.store
            },
            'find': {
                'description': 'find credentials of a particular app',
                'action': self.find
            },
            'delete data': {
                'description': 'delete credentials of a particular app',
                'action': self.delete_credentials
            },
            'update data': {
                'description': 'update credentials of a particular app',
                'action': self.update_credentials
            },
            'delete account': {
                'description': 'delete your account',
                'action': self.delete_account
            },
            'update account': {
                'description': 'update your account',
                'action': self.update_account
            },
            'show': {
                'description': 'show all credentials',
                'action': self.show
            }
        }

        self.db = database

    def __help(self):
        for count, command in enumerate(self.commands_list.items(), 1):
            print(f'{count}. "{command[0]}": {command[1]["description"]}')

    @logged
    def show(self):
        self.db.show_all_credentials()

    def login(self):
        if not self.db.logged:
            password = input('Enter your password: ')

            while not self.db.find_user(password):
                password = input('Enter your password: ')
        else:
            print('\u001b[32m' + "You're already logged in!" + '\u001b[0m')

    def register(self):
        name = input('Enter your username (required): ')
        password = getpass('Enter your password (required): ')

        if name and password:
            while not self.db.create_user(name, password):
                password = input('Enter your password: ')

    def exit(self):
        exit(0)

    @logged
    def logout(self):
        self.db.logout()

    @logged
    def store(self):
        app_name = input('Fill in the name of your app or website (required): ')

        if app_name:
            username = input('If there is a username, type it here: ')
            email = input('If there is an email or a login, type it here: ')
            password = input('Fill in the password: ')

            while not self.db.store_credentials(app_name, email, password, username):
                username = input('If there is a username, type it here: ')
                email = input('If there is an email or a login, type it here: ')
                password = input('Fill in the password: ')

    @logged
    def find(self):
        app_name = input('Fill in the name of your app or website: ')

        if app_name:
            while not self.db.find_credentials(app_name):
                app_name = input('Fill in the name of your app or website: ')

    @logged
    def delete_account(self):
        choice = input('\u001b[31m' + 'Precaution! This will also delete all your data! Are you sure? ("yes" or "no"): '  + '\u001b[0m')

        if choice == 'yes':
            self.db.delete_user()

    @logged
    def update_account(self):
        property_to_be_updated = input('What property do you wanna update? ("name" or "password"): ')

        if property_to_be_updated == 'name' or property_to_be_updated == 'password':
            new_value = input(f'New {property_to_be_updated}: ')

            while not self.db.update_user(property_to_be_updated, new_value):
                new_value = input('New value: ')

    @logged
    def delete_credentials(self):
        app_name = input('Fill in the name of what you wanna delete: ')

        if app_name:
            while not self.db.delete_credentials(app_name):
                app_name = input('Fill in the name of what you wanna delete: ')

    @logged
    def update_credentials(self):
        app_name = input('Fill in the name of what you wanna update: ')

        if app_name:
            while not self.db.find_credentials(app_name):
                app_name = input('Fill in the name of what you wanna update: ')

            property_to_be_updated = input('What property do you wanna update ("app name", "email", "password", "username"): ')

            if property_to_be_updated:
                new_value = input(f'New {property_to_be_updated}: ')

                if property_to_be_updated == 'app name':
                    property_to_be_updated = property_to_be_updated.replace(' ', '_')

                while not self.db.update_credentials(app_name, property_to_be_updated, new_value):
                    property_to_be_updated = input('What property do you wanna update: ')
                    new_value = input('New value: ')