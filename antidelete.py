#When a user deletes a message in a specificed group chat, this script will re-broadcast the deleted message

from fbchat import Client
from fbchat.models import *
import getpass,string
from collections import deque

recent=deque([])
sentMessages=dict()
class archiveBot(Client):
    def onMessage(self,mid,author_id,message_object,thread_id,thread_type,ts,**kwargs):
        if int(thread_id)==targetThread:
            #message_text="".join(filter(lambda x: x in string.printable,message_object.text))
            sentMessages[mid]=message_object.text
            recent.append(mid)
            print("Added MID '{}' and text '{}' to dictionary".format(mid,message_object.text))
            if len(recent)>100:
                old_mid=recent.popleft()
                print("Deleted MID '{}' and text '{}' from dictionary".format(old_mid,sentMessages[old_mid]))
                del sentMessages[old_mid]
    def onMessageUnsent(self,mid,author_id,thread_id,thread_type,**kwargs):
        if int(thread_id)==targetThread:
            if mid in sentMessages:
                newuser=self.fetchUserInfo(str(author_id))[str(author_id)]
                send_msg="{} has removed the following message: '{}'".format(newuser.first_name,sentMessages[mid])
                print(send_msg)
                self.sendMessage(send_msg,thread_id=thread_id,thread_type=thread_type)
targetThread=int(input("Target Thread? "))
email = input("Email address? ")
client = archiveBot(email,getpass.getpass())
client.listen()
