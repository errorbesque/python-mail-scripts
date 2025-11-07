from protonmail import ProtonMail
from datetime import datetime
import math

username='username'
password='password'

proton = ProtonMail()

try:
    proton.login(username, password)

    # get list of distinct emails before a certain date
    pagesize=150
    messages_count=proton.get_messages_count()
    names_test = []
    count=pagesize
    i=0
    while count>=pagesize:
        messages = proton.get_messages_by_page(i,150)
        for m in messages:
            # message = proton.read_message(m)
            if m.time < datetime(2025,11,5,0,0).timestamp():
                print(f"{m.sender.address} / {m.subject} / {datetime.fromtimestamp(m.time)}")
                names_test.append(m.sender.address)
        count=len(messages)
        i+=1

    distinct_names = list(set(names_test))
    print(distinct_names)

    names_on_the_list = ['email1@gmail.com','email2@gmail.com']

    subject="Rave Response"
    html="This is the response we give to people already on the list."
    try:
        while True: # sry idk how to do/while in python  
            new_message = proton.wait_for_new_message(interval=1, timeout=0, rise_timeout=False, read_message=True)
            if new_message.sender.address in names_on_the_list:
                # received new mail from a person on the list
                message_to_send = proton.create_message(
                recipients=[new_message.sender.address],
                bcc=["bccemail@gmail.com"], # can choose to alert us via bcc 
                subject=subject,
                body=html,  # can be html or plaintext
                in_reply_to=new_message.id,
                )
                sent_message = proton.send_message(message_to_send)
                print(f"sent message to {new_message.sender.address}")
            else:
                print(f"sender was {new_message.sender.address}; try it again\n")
    except:
        print("trying while loop again")
except:
    print("error at ")
    print(datetime.fromtimestamp(datetime.now()))
