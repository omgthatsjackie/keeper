from hashlib import pbkdf2_hmac

salt = b'bruhbruhbruh'

def hash_password(password):
    return pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()[0:50]