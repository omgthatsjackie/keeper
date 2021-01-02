from variables import variables
from models.commands import Commands
from models.database import Database

db = Database(
    user=variables['DB_USERNAME'],
    password=variables['DB_PASSWORD'],
    host=variables['DB_HOST'],
    database=variables['DB_NAME']
)

commands = Commands(db)

print('\u001b[33m' + 'Welcome to Keeper!' + '\u001b[32m' + '\n\nType in the command below (type "help" to get the list of all commands)\n' + '\u001b[0m')

with open('./.cache') as cache:
    data = cache.read()

    if data:
        parsed = data.split()
        db.logged = True
        db.user_id = int(parsed[1])
        print('\u001b[32m' + f'Logged as {parsed[0]}\n' + '\u001b[0m')

while True:
    choice = input(': ').lower().strip()

    if choice in commands.commands_list:
        commands.commands_list[choice]['action']()
    else:
        print('\u001b[31m' + 'No such command!' + '\u001b[0m')