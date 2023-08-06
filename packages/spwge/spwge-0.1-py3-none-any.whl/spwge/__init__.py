# import the necessary modules!
import secrets
import string

print('Welcome to Password generator')

#input the length of password
length = int(input('\nEnter the length of password: '))                      

#define data
lower = string.ascii_lowercase
upper = string.ascii_uppercase
num = string.digits
symbols = string.punctuation

# combine the data
overall = lower + upper + num + symbols

#use secrets 
password = ''.join(secrets.choice(overall) for i in range(length))  

#print the password
print(password)