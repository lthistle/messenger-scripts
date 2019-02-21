import json, pickle, time, sys, os, getpass
from collections import deque
from fbchat import Client
from fbchat.models import *
import requests, gnupg

IMAGEDIR = 'temp_images/'

def setup_settings():
    params = {"username": "What is your username",
              "pass": "What is your password / path to file with your password (leave blank to use getpass)",
             }
    data = {param: input(params[param] + "? ").strip() for param in params}
    data["threads"] = []
    with open("config.json", "w") as f:
        json.dump(data, f)

def get_pass(fname): return str(gpg.decrypt_file(open(fname, "rb"))).split()[0]

def load_file(fname, func):
    try:
        with open(fname) as f:
            return func(f)
    except FileNotFoundError:
        return {}

def make_client():
    try:
        client = archiveBot(CONFIG["username"], get_pass(CONFIG["pass"]) if len(CONFIG["pass"]) > 0 else getpass.getpass(), session_cookies=COOKIE)
        with open("cookie.gpg", "w") as f:
            f.write(str(gpg.encrypt(pickle.dumps(client.getSession()), KEYID)))
    except:
        client = archiveBot(CONFIG["username"], get_pass(CONFIG["pass"]) if len(CONFIG["pass"]) > 0 else getpass.getpass())
    return client

class archiveBot(Client):

    def init(self):
        self.recent, self.sentMessages = deque([]), {}
        self.targetThreads = CONFIG["threads"] if len(CONFIG["threads"]) > 0 else [input("Target Thread? ")]

    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, **kwargs):
        if thread_id in self.targetThreads:
            mid = mid[5:]
            self.sentMessages[mid] = message_object.text
            self.recent.append(mid)
            print(f"Added MID '{mid}' and text '{message_object.text}' to dictionary")
            pos = 0
            for sentFile in message_object.attachments:
                if isinstance(sentFile,ImageAttachment):
                    img_data = requests.get(self.fetchImageUrl(sentFile.uid)).content
                    with open(f"{IMAGEDIR + mid + '_'}{pos}.jpg",'wb') as handler:
                        handler.write(img_data)
                    pos += 1
            if len(self.recent) > 100:
                old_mid = self.recent.popleft()
                print(f"Deleted MID '{old_mid}' and text '{self.sentMessages[old_mid]}'")
                for filename in os.listdir(IMAGEDIR):
                    if filename.startswith(old_mid):
                        os.remove(IMAGEDIR + filename)
                del self.sentMessages[old_mid]

    def onMessageUnsent(self, mid, author_id, thread_id, thread_type, **kwargs):
        if thread_id in self.targetThreads:
            mid = mid[5:]
            if mid in self.sentMessages:
                newuser = self.fetchUserInfo(str(author_id))[str(author_id)]
                send_msg = "{} has removed the following message: '{}'".format(newuser.first_name, self.sentMessages[mid] if self.sentMessages[mid] is not None else "")
                print(send_msg)
                self.sendMessage(send_msg, thread_id=thread_id, thread_type=thread_type)
                for filename in os.listdir(IMAGEDIR):
                    if filename.startswith(mid):
                        print(IMAGEDIR + filename)
                        self.sendLocalImage(IMAGEDIR + filename, message=Message(), thread_id=thread_id, thread_type=thread_type)
                        time.sleep(0.2)

if len(sys.argv) > 1 and sys.argv[1] == "setup":
    setup_settings()

CONFIG = load_file("config.json", lambda x: json.load(x))

try:
    gpg = gnupg.GPG()
    KEYID = gpg.list_keys(True)[0]['keyid']
    COOKIE = load_file("cookie.gpg", lambda x: pickle.loads(gpg.decrypt(x.read()).data))
except:
    pass

if __name__ == "__main__":

    if not os.path.isdir(IMAGEDIR):
        os.mkdir(IMAGEDIR)

    client = make_client()
    client.init()
    client.listen()
