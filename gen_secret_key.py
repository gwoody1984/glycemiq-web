from base64 import b64encode
from os import urandom

random_bytes = urandom(64)
print(b64encode(random_bytes).decode('utf-8'))