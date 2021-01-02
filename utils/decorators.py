from functools import wraps

def logged(func):
    @wraps(func)
    def wrapper(self):
        if self.db.logged:
            func(self)
        else:
            print('\u001b[32m' + 'You have to be logged in:)' + '\u001b[0m')

    return wrapper