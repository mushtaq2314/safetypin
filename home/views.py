from django.shortcuts import render,HttpResponse
from home.models import SignUP
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import ast
#encode into image
from PIL import Image
import os
import sys
import os.path
from os import path

def convertToRGB(img):
	try:
		rgba_image = img
		rgba_image.load()
		background = Image.new("RGB", rgba_image.size, (255, 255, 255))
		background.paste(rgba_image, mask = rgba_image.split()[3])
		return background
	except Exception as e:
		print("[red]Couldn't convert image to RGB [/red]- %s"%e)


def getPixelCount(img):
	width, height = Image.open(img).size
	return width*height


def encodeImage(image,message,filename):
		try:
			width, height = image.size
			pix = image.getdata()

			current_pixel = 0 #start from beginning
			tmp=0 #counter

			x=0
			y=0
			for ch in message:
				binary_value = format(ord(ch), '08b')
				
				# For each character, get 3 pixels at a time
				p1 = pix[current_pixel]
				p2 = pix[current_pixel+1]
				p3 = pix[current_pixel+2]

				three_pixels = [val for val in p1+p2+p3] #make them as one list

				for i in range(0,8):
					current_bit = binary_value[i]

					# 0 - Even
					# 1 - Odd
					if current_bit == '0':
						if three_pixels[i]%2!=0:
							three_pixels[i]= three_pixels[i]-1 if three_pixels[i]==255 else three_pixels[i]+1
					elif current_bit == '1':
						if three_pixels[i]%2==0:
							three_pixels[i]= three_pixels[i]-1 if three_pixels[i]==255 else three_pixels[i]+1

				current_pixel+=3 #take next set of pixels
				tmp+=1 #increment counter

				#Set 9th value
				if(tmp==len(message)):
					# Make as 1 (odd) - stop reading
					if three_pixels[-1]%2==0:
						three_pixels[-1]= three_pixels[-1]-1 if three_pixels[-1]==255 else three_pixels[-1]+1
				else:
					# Make as 0 (even) - continue reading
					if three_pixels[-1]%2!=0:
						three_pixels[-1]= three_pixels[-1]-1 if three_pixels[-1]==255 else three_pixels[-1]+1


				three_pixels = tuple(three_pixels)
				
				st=0
				end=3

				for i in range(0,3): #modifying pixels 
					image.putpixel((x,y), three_pixels[st:end])
					st+=3
					end+=3

					if (x == width - 1):
						x = 0
						y += 1
					else:
						x += 1

			encoded_filename = filename.split('.')[0] + "-enc.png"
			image.save(encoded_filename)
			print("\n")
			print("[yellow]Original File: [u]%s[/u][/yellow]"%filename)
			print("[green]Image encoded and saved as [u][bold]%s[/green][/u][/bold]"%encoded_filename)

		except Exception as e:
			print("[red]An error occured - [/red]%s"%e)
			sys.exit(0)



def decodeImage(image):
		try:
			pix = image.getdata()
			current_pixel = 0
			decoded=""
			while True:
				# Get 3 pixels each time
				binary_value=""
				p1 = pix[current_pixel]
				p2 = pix[current_pixel+1]
				p3 = pix[current_pixel+2]
				three_pixels = [val for val in p1+p2+p3] #make them as one list

				for i in range(0,8):
					if three_pixels[i]%2==0:
						# add 0 to msg
						binary_value+="0"
					elif three_pixels[i]%2!=0:
						# add 1 to msg
						binary_value+="1"


				#Convert binary value to ascii and add to string
				binary_value.strip() #strip removes spaces
				ascii_value = int(binary_value,2)
				decoded+=chr(ascii_value)
				current_pixel+=3

				if three_pixels[-1]%2!=0:
					#last letter termination
					break

			# print("Decoded: %s"%decoded)
			return decoded
		except Exception as e:
			print("[red]An error occured - [/red]%s"%e)
			sys.exit()



#####################################################################################
#Steganography
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import base64
global encpwd
encpwd="qwerty"
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
########################################################################################    


# Create your views here.

def index(request):
    
    return render(request,'index.html')


def Login(request):
    if request.method == "POST":
        global lmail
        lmail = request.POST.get('lmail')
        lpass = request.POST.get('lpass')
        
        mails = list(SignUP.objects.values_list('email',flat=True))
        passwords = list(SignUP.objects.values_list('password',flat=True))

        if lmail in mails:
            k = mails.index(lmail)
            if decrypt(encpwd.encode(),str(passwords[k])).decode()==lpass:
                ####################################
                global nm
                nm = list(list(SignUP.objects.filter(email=lmail).values_list('name'))[0])[0]
                ####################################
                context = {'name':nm}
                
                return render(request,'home.html',context)
            else:
                context = {'message':'Invalid Credentials.Try Again'}
                return render(request,'login.html',context)
        else:
                context = {'message':'Invalid Credentials.Try Again'}
                return render(request,'login.html',context)

    return render(request,'login.html')

def generate(request):
    return render(request,'generate.html')

def signup(request):
    allmails = list(SignUP.objects.values_list('email',flat=True))
    if request.method == "POST":
        name = request.POST.get('sname')
        global email
        email = request.POST.get('smail')
        password = request.POST.get('spass')
        if email in allmails:
            return render(request,'signup.html',{'message':'Email already exists'})
        else:    
            print(name,email,password)
            signup = SignUP(name= name,email = email,password=encrypt(encpwd.encode(),password.encode()),image = "C:/Users/DELL/Desktop/Django/first/images/img19_1920x1200.jpg")    
            signup.save()
            context = {'name':name}
            return render(request,'login.html',context)
    return render(request,'signup.html')


##################
def forgot(request):
    return render(request,'forgot.html')

def help(request):
    return render(request,'help.html')

def store(request):
    global lmail
    data = list(list(SignUP.objects.filter(email=lmail).values_list())[0])
    context={"passwords":ast.literal_eval(decrypt(encpwd.encode(),str(data[-1])).decode())}
    modify = ast.literal_eval(decrypt(encpwd.encode(),str(data[-1])).decode())
    
    # print(modify)
    x = Image.open("C:/Users/DELL/Desktop/Django/first/images/img19_1920x1200.jpg")
    y = x.copy()
    if (request.method=='POST'):
        l=[ request.POST.get('1'),
         request.POST.get('2'),
         request.POST.get('3'),
         request.POST.get('4'),
         request.POST.get('5'),
         request.POST.get('6'),
         request.POST.get('7'),
         request.POST.get('8')]
        c=0 
        for i in modify.keys():
            if(l[c] is not 'None'):
                modify.update({i:l[c]})
            c+=1
        # print(modify) 
        for i in modify.keys():
            if modify[i]=='None':
                modify[i]=None
        msg = str(modify)
        # print(str(modify))
        encodeImage(y,encrypt(encpwd.encode(),msg.encode()),x.filename)
        SignUP.objects.filter(email=lmail).update(passwords=encrypt(encpwd.encode(),msg.encode()))
        SignUP.objects.filter(email=lmail).update(image='img19_1920x1200-enc.png')   
        data = list(list(SignUP.objects.filter(email=lmail).values_list())[0])
        context={"passwords":ast.literal_eval(decrypt(encpwd.encode(),str(data[-1])).decode())}
    return render(request,'store.html',context)
def wallet(request):
    return render(request,'wallet.html') 
def passwords(request):
    global lmail
    data = list(list(SignUP.objects.filter(email=lmail).values_list())[0])
    print("passwords : ",data[-1])
    print(type(data[-1]))
    # str = decrypt_message(data[-1])
    # print(str)
    context={"passwords":ast.literal_eval(decrypt(encpwd.encode(),str(data[-1])).decode())}
    print(context)
    print(type(context))
    return render(request,'passwords.html',context)        

def contact(request):
    return render(request,'contact.html')

def profile(request):
    try:
        global lmail
        data = list(list(SignUP.objects.filter(email=lmail).values_list())[0])
        context={'name':data[1],'mail':data[2],'phone':data[5],'dob':data[7],'gender':data[6]}
        print(data)
        if request.method=='POST':
            name=request.POST.get('name')
            mail=request.POST.get('mail')
            phone=request.POST.get('phone')
            dob=request.POST.get('dob')
            gender = request.POST.get('gender')
            SignUP.objects.filter(email=lmail).update(name=name,phone=phone,DOB=dob,gender=gender)
            data = list(list(SignUP.objects.filter(email=lmail).values_list())[0])
            context={'name':data[1],'mail':data[2],'phone':data[5],'dob':data[7],'gender':data[6]}
        # if request.method=='POST':
        #     return render(request,'index.html')    
        return render(request,'profile.html',context)
    except:
        global email
        data = list(list(SignUP.objects.filter(email=email).values_list())[0])
        context={'name':data[1],'mail':data[2],'phone':data[5],'dob':data[7]}
        print(data)
        return render(request,'profile.html',context)
         

def home(request):
    global nm
    context = {'name':nm}
    return render(request,'home.html',context)

def services(request):
    return render(request,'services.html')
