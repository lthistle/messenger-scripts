#Prompts you to log in to create a login.ck file which contains session session cookies
from fbchat import Client
import getpass,pickle

email=input("Email address? ")
client = Client(email,getpass.getpass())
pickle.dump(client.getSession(),open('login.ck','wb'))
print("Local login.ck session cookie file made")
