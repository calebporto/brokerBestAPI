import secrets
import string

def generate_secret_key(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret_key

# Example usage: generate a 32-character secret key including punctuation
secret_key = generate_secret_key(32)
print(secret_key)