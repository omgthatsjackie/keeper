import psycopg2
from secrets import randbelow
from utils.hashing import hash_password

class Database:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.logged = False
        self.user_id = 0

    def __generate_id(self):
        return randbelow(10000)

    def __connect(self):
        try:
            connection = psycopg2.connect(user=self.user, password=self.password, host=self.host, database=self.database)

            return connection

        except (Exception, psycopg2.Error) as error:
            print(error)

    def __check_data(self, connection, cursor, app_name=None):
        if app_name:
            select_query = 'SELECT email, password, username FROM accounts WHERE user_id = %s AND app_name = %s'
            record_to_select = (self.user_id, app_name)
        else:
            select_query = 'SELECT * FROM accounts WHERE user_id = %s'
            record_to_select = (self.user_id,)

        cursor.execute(select_query, record_to_select)
        connection.commit()
        credentials = cursor.fetchone()

        return credentials

    def create_user(self, name, password):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            insert_query = 'INSERT INTO users (name, password, id) VALUES (%s, %s, %s)'
            user_id = self.__generate_id()
            hashed_password = hash_password(password)
            record_to_insert = (name, hashed_password, user_id)
            cursor.execute(insert_query, record_to_insert)
            connection.commit()

            print('\u001b[32m' + 'Account is successfully created!' + '\u001b[0m')

            return True

        except (Exception, psycopg2.Error):
            print('\u001b[31m' + 'Password is already being used, try another one!' + '\u001b[0m')

            return False

    def find_user(self, password):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            select_query = 'SELECT name, id FROM users WHERE password = %s'
            hashed_password = hash_password(password)
            record_to_select = (hashed_password,)
            cursor.execute(select_query, record_to_select)
            connection.commit()
            data = cursor.fetchone()
            self.logged = True
            self.user_id = data[1]

            with open('./.cache', 'w') as cache:
                cache.write(f'{data[0]} {self.user_id}')

            print('\u001b[32m' + f'Logged in as {data[0]}' + '\u001b[0m')

            return True

        except (Exception, psycopg2.Error):
            print('\u001b[31m' + 'User not found, try again!' + '\u001b[0m')

            return False

    def delete_user(self):
        try:
            connection = self.__connect()
            cursor = connection.cursor()

            delete_query_1 = 'DELETE FROM accounts WHERE user_id = %s'
            record_to_delete = (self.user_id,)
            cursor.execute(delete_query_1, record_to_delete)
            connection.commit()

            delete_query_2 = 'DELETE FROM users WHERE id = %s'
            record_to_delete = (self.user_id,)
            cursor.execute(delete_query_2, record_to_delete)
            connection.commit()

            self.logged = False
            self.user_id = 0

            with open('./.cache', 'r+') as cache:
                cache.truncate(0)

            print('\u001b[32m' + f'Your account is successfully deleted!' + '\u001b[0m')

        except (Exception, psycopg2.Error):
            print('\u001b[31m' + 'Something went wrong, try again!' + '\u001b[0m')

    def update_user(self, property_to_be_updated, new_value):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            update_query = f'UPDATE users SET {property_to_be_updated} = %s WHERE id = %s'

            if property_to_be_updated == 'password':
                hashed_password = hash_password(new_value)
                record_to_update = (hashed_password, self.user_id)
            else:
                record_to_update = (new_value, self.user_id)

            cursor.execute(update_query, record_to_update)
            connection.commit()

            print('\u001b[32m' + 'Successfully updated!' + '\u001b[0m')

            return True

        except (Exception, psycopg2.Error):
            print('\u001b[31m' + 'Something went wrong, try again!' + '\u001b[0m')

            return False

    def logout(self):
        self.logged = False
        self.user_id = 0

        print('\u001b[32m' + 'Successfully logged out!' + '\u001b[0m')

        with open('./.cache', 'r+') as cache:
            cache.truncate(0)

    def store_credentials(self, app_name, email, password, username):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            insert_query = 'INSERT INTO accounts VALUES (%s, %s, %s, %s, %s)'
            record_to_insert = (app_name, email, password, username, self.user_id)
            cursor.execute(insert_query, record_to_insert)
            connection.commit()

            print('\u001b[32m' + 'Stored successfully!' + '\u001b[0m')

            return True

        except (Exception, psycopg2.Error):
            print('\u001b[31m' + 'Something went wrong, try again!' + '\u001b[0m')

            return False

    def show_all_credentials(self):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            select_query = 'SELECT app_name, email, password, username FROM accounts WHERE user_id = %s'
            record_to_select = (self.user_id,)
            cursor.execute(select_query, record_to_select)
            connection.commit()
            accounts = cursor.fetchall()

            if accounts:
                for app_name, email, password, username in accounts:
                    print(f'App name: {app_name}\nEmail: {email}\nPassword: {password}\nUsername: {username}\n')
            else:
                print('\u001b[32m' + "You don't have any credentials added yet..." + '\u001b[0m')

        except (Exception, psycopg2.Error):
            print('\u001b[31m' + 'Something went wrong, try again!' + '\u001b[0m')

    def find_credentials(self, app_name):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            select_query = 'SELECT email, password, username FROM accounts WHERE user_id = %s AND app_name = %s'
            record_to_select = (self.user_id, app_name)
            cursor.execute(select_query, record_to_select)
            connection.commit()
            credentials = cursor.fetchone()

            if not self.__check_data(connection, cursor):
                print('\u001b[32m' + "You don't have any credentials added yet..." + '\u001b[0m')
            elif credentials:
                print(f'App name: {app_name}\nEmail: {credentials[0]}\nPassword: {credentials[1]}\nUsername: {credentials[2]}')
            else:
                print('\u001b[32m' + "You haven't added this app!" + '\u001b[0m')

            return True

        except (Exception, psycopg2.Error):
            print('\u001b[31m' + 'Try again!' + '\u001b[0m')

            return False

    def delete_credentials(self, app_name):
        try:
            connection = self.__connect()
            cursor = connection.cursor()

            if not self.__check_data(connection, cursor):
                print('\u001b[32m' + 'Nothing to delete...' + '\u001b[0m')
            elif self.__check_data(connection, cursor, app_name):
                delete_query = 'DELETE FROM accounts WHERE app_name = %s AND user_id = %s'
                record_to_delete = (app_name, self.user_id)
                cursor.execute(delete_query, record_to_delete)
                connection.commit()

                print('\u001b[32m' + 'Successfully deleted!' + '\u001b[0m')
            else:
                print('\u001b[32m' + "You haven't added this app!" + '\u001b[0m')

            return True

        except (Exception, psycopg2.Error):
            print('\u001b[31m' + 'Something went wrong, try again!' + '\u001b[0m')

            return False


    def update_credentials(self, app_name, property_to_be_updated, new_value):
        try:
            connection = self.__connect()
            cursor = connection.cursor()
            update_query = f'UPDATE accounts SET {property_to_be_updated} = %s WHERE app_name = %s AND user_id = %s'
            record_to_update = (new_value, app_name, self.user_id)
            cursor.execute(update_query, record_to_update)
            connection.commit()

            print('\u001b[32m' + 'Successfully updated!' + '\u001b[0m')

            return True

        except (Exception, psycopg2.Error):
            print('\u001b[31m' + 'Try again' + '\u001b[0m')

            return False
