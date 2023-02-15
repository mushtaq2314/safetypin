import ast
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import base64
def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate Initialization vector
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode() if encode else data


def decrypt(key, source, decode=True):
    if decode:
        source = base64.b64decode(source.encode())
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the Initialization vector from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding

password = "qwerty"
message = "{'Facebook':None,'Instagram':None,'Twitter':None,'Dropbox':None,'Google':None,'Spotify':None,'GitHub':None,'Snapchat':None}"
cipher=encrypt(password.encode(),message.encode())
print("Cipher : ",cipher,type(cipher))


# decoded=decrypt(password.encode(),cipher)
# print("Decoded :",decoded,decoded.decode())
# print(type(decoded))
# print(type(decoded.decode()))
# print(decoded.decode(),type(decoded.decode()))
# print(ast.literal_eval(decoded.decode()),type(ast.literal_eval(decoded.decode())))
# print((decrypt(password.encode(),'f/9Zap2kUfojri6SltJsW0JERpx+UgV5BHNKHGz6Sd7y1EWXk5QkE5yCo4xCCnOjisaWsnSP6bAnlIf87t1OW5ycncoNxW////V0fRLd9G+GzWZp/dsnzLgO+6/yMXG0c8lKTn/ted2Q03KLaPoB6oh3zTyEHQmfZzSS6/r+/Z3fuUh0nzmf12ioRMp5AU53')).decode())
# # print(encrypt(password.encode()))
# # print(decrypt(password.encode(),'M04kifxrYCKTCrQ7WzYZSCBbLqvAHZtALsLuKOwQ/ORlPo0pOPWD3+Qv9AFLlHi+lT8uYNyHN0JBEKxsgaHQsoONwrXvEU8Duis8i3NRPvftL1yvvX6hNMxIZJXgq7SZFfjQfAQhE38sowdCU2hzleEBfvLEWWHGRQljm/YYnJ/kRX/btc6Wz3zpuaGsPBm24kOqkKPpYBi/3uNWePmjSvqxzZ7kOpuSR35Rw+IoAhQ='))
