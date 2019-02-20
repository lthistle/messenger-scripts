#Commonly used methods
from fbchat import Client
import pickle,getpass
def get_session():
    useCookie=input("Use local session_cookie file to log in (Y/N)? ").lower()
    if useCookie=='y':
        try:
            return pickle.load(open('session_cookie','rb'))
        except:
            print("Could not find session_cookie file or file was corrupted, please log in manually.")
    email=input("Email address? ")
    c = Client(email,getpass.getpass())
    return c.getSession()
