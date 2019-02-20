#Commonly used methods
from fbchat import Client
import pickle,getpass
def login_client():
    useCookie=input("Use local session_cookie file to log in (Y/N)? ").lower()
    if useCookie=='y':
        try:
            return Client('','',session_cookies=pickle.load(open('session_cookie','rb')))
        except:
            print("Could not find session_cookie file, please log in manually.")
    email=input("Email address? ")
    return Client(email,getpass.getpass())

login_client().listen()
