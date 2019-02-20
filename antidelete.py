#When a user deletes a message in a specificed group chat, this script will re-broadcast the deleted message
from fbchat import Client
from fbchat.models import *
import getpass,time,os,requests,utils
from collections import deque

recent=deque([])
sentMessages=dict()

imagedir='temp_images/'
if not os.path.isdir(imagedir):
    os.mkdir(imagedir)

class archiveBot(Client):
    def onMessage(self,mid,author_id,message_object,thread_id,thread_type,ts,**kwargs):
        if int(thread_id)==targetThread and author_id!=self.uid:
            mid=mid[5:]
            sentMessages[mid]=message_object.text
            recent.append(mid)
            print("Added MID '{}' and text '{}' to dictionary".format(mid,message_object.text))
            pos=0
            print('length is '+str(len(message_object.attachments)))
            for sentFile in message_object.attachments:
                if isinstance(sentFile,ImageAttachment):
                    fileprefix=imagedir+mid+'_'
                    time.sleep(0.2)
                    print(self.fetchImageUrl(sentFile.uid))
                    img_data=requests.get(self.fetchImageUrl(sentFile.uid)).content
                    with open(fileprefix+str(pos)+'.jpg','wb') as handler:
                        handler.write(img_data)
                    pos+=1
            if len(recent)>100:
                old_mid=recent.popleft()
                print("Deleted MID '{}' and text '{}' from dictionary".format(old_mid,sentMessages[old_mid]))
                for filename in os.listdir(imagedir):
                    if filename.startswith(old_mid):
                        os.remove(imagedir+filename)
                del sentMessages[old_mid]

    def onMessageUnsent(self,mid,author_id,thread_id,thread_type,**kwargs):
        if int(thread_id)==targetThread:
            mid=mid[5:]
            if mid in sentMessages:
                newuser=self.fetchUserInfo(str(author_id))[str(author_id)]
                send_msg="{} has removed the following message: '{}'".format(newuser.first_name,sentMessages[mid])
                print(send_msg)
                self.sendMessage(send_msg,thread_id=thread_id,thread_type=thread_type)
                for filename in os.listdir(imagedir):
                    if filename.startswith(mid):
                        print(imagedir+filename)
                        self.sendLocalImage(imagedir+filename,message=Message(),thread_id=thread_id,thread_type=thread_type)
                        time.sleep(0.2)
targetThread=int(input("Target Thread? "))
client = archiveBot('','',session_cookies=utils.get_session())
client.listen()
