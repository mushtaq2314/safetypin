
message = "{'Facebook':None,'Instagram':None,'Twitter':None,'Dropbox':None,'Google':None,'Spotify':None,'GitHub':None,'Snapchat':None}"
cipher=encrypt(password.encode(),message.encode())
print("Cipher : ",cipher,type(cipher))