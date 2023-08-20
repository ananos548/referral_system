import random
import string


def generate_invite_code():
    return ''.join(random.choices(string.digits + string.ascii_letters, k=6))


def generate_auth_code():
    return ''.join(random.choices(string.digits, k=4))
