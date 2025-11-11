from protonmail import ProtonMail
from datetime import datetime
import math
import time
import pickle
import pandas as pd
import csv

username= 'username'
password= 'password'

get_new_distinct_names = False
distinct_names=[]

captchafailure=datetime.now()
captchamultiplier=2

html_for_others="""
<html><body>
This is what we send to people not on the list.
</body></html>"""

html_for_list="""
<html><body>
This is what we send to people who are on the list.
</body></html>"""

proton = ProtonMail()

if True: # only do this if i need to login
    proton.login(username, password)
    proton.save_session('session.pickle')

while True:
    try:
        proton.load_session('session.pickle')
        captchamultiplier=2 # reset captcha multiplier on success

        if get_new_distinct_names:
            # get list of distinct emails
            pagesize=150
            names_test = []
            count=pagesize
            i=0
            while count>=pagesize:
                messages = proton.get_messages_by_page(i,pagesize)
                for m in messages:
                    # message = proton.read_message(m) # only need this if you're reading the body
                    if m.time < datetime(2025,11,5,0,0).timestamp():
                        # print(f"{m.sender.address} / {m.subject} / {datetime.fromtimestamp(m.time)}")
                        names_test.append(m.sender.address)
                count=len(messages)
                i+=1
            
            distinct_names = set(names_test)
            print(distinct_names)
            pickle.dump(distinct_names, open("save.p","wb"))
        else:
            # distinct_names = pickle.load(open("save.p","rb"))
            with open('handlist.csv', newline='') as inputfile:
                for row in csv.reader(inputfile):
                    distinct_names.append(row[0])
            distinct_names=set(distinct_names)
        
        # range assignments
        events = [
            {'startdate': datetime(2025,10,15), 'enddate': datetime(2025,11,9), 'eventname': 'Event1'},
            {'startdate': datetime(2024,2,1), 'enddate': datetime(2024,3,24), 'eventname': 'Event2'},
            {'startdate': datetime(2024,10,1), 'enddate': datetime(2024,11,3), 'eventname': 'Event3'},
            {'startdate': datetime(2023,2,1), 'enddate': datetime(2023,3,18), 'eventname': 'Event4'},
            {'startdate': datetime(2023,7,1), 'enddate': datetime(2023,8,6), 'eventname': 'Event4'},
            {'startdate': datetime(2022,10,1), 'enddate': datetime(2022,10,30), 'eventname': 'Event5'}]
        
        eventdata = []
        
        # create eventdata and count oldsenders vs newsenders 
        names_test = []
        pagesize=150
        count=pagesize
        i=0
        oldsenders=0
        newsenders=0
        newnames = []
        while count>=pagesize:
            messages = proton.get_messages_by_page(i,pagesize)
            for m in messages:
                # categorize into old events
                for event in events:
                    if event['startdate'].timestamp() <= m.time <= event['enddate'].timestamp():
                        eventdata.append({'time':m.time, 'event':event['eventname'], 'sender':m.sender.address, 'timeuntilevent': event['enddate'].timestamp()-m.time })
                if m.time > datetime(2025,11,5,0,0).timestamp():
                    if m.sender.address in distinct_names:
                        oldsenders+=1
                        print(f"{math.floor(100*oldsenders/(newsenders+oldsenders))}% / OLD_SENDER {m.sender.address} / {m.subject} / {datetime.fromtimestamp(m.time)}")
                    else:
                        newsenders+=1
                        newnames.append(m.sender.address)
                        print(f"{math.floor(100*oldsenders/(newsenders+oldsenders))}% / NEW_SENDER {m.sender.address} / {m.subject} / {datetime.fromtimestamp(m.time)}")
            count=len(messages)
            i+=1
            
        df = pd.DataFrame(eventdata)
        pickle.dump(eventdata, open("eventdata.p","wb"))

        names_on_the_list = distinct_names
        # names_on_the_list = set(['rgruver@gmail.com','faitpoms@gmail.com'])

        subject="subject"
        
        while True: 
            try:
                new_message = proton.wait_for_new_message(interval=1, timeout=0, rise_timeout=False, read_message=True)
                # eventdata.append({'time':m.time, 'event': event[0]['eventname'], 'sender':m.sender.address, 'timeuntilevent': event[0]['enddate'].timestamp()-m.time }) # append to samhain
                df = pd.DataFrame(eventdata)
                pickle.dump(eventdata, open("eventdata.p","wb"))

                if new_message.sender.address in names_on_the_list:
                    # received new mail from a person on the list
                    message_to_send = proton.create_message(
                    recipients=[new_message.sender.address],
                    subject=subject,
                    body=html_for_list,  # can be html or plaintext
                    in_reply_to=new_message.id,
                    )
                    sent_message = proton.send_message(message_to_send)
                    print(f"sent message to {new_message.sender.address}")
                else:
                    message_to_send = proton.create_message(
                    recipients=[new_message.sender.address],
                    # bcc=["rgruver@protonmail.com"], # can choose to alert us via bcc 
                    subject=subject,
                    body=html_for_others,  # can be html or plaintext
                    in_reply_to=new_message.id,
                    )
                    sent_message = proton.send_message(message_to_send)
                    print(f"sender was {new_message.sender.address}; try it again\n")
                    if new_message.sender.address in distinct_names:
                        oldsenders+=1
                    else:
                        newsenders+=1
                    print(f"{math.floor(100*oldsenders/(newsenders+oldsenders))}% old senders / {new_message.sender.address} / {new_message.subject} / {datetime.fromtimestamp(new_message.time)}")
            except KeyboardInterrupt:
                print("keyboard interrupt")
                break
            except Exception as e: 
                print(e)
                print("trying twait for new message again")
    except KeyboardInterrupt:
        print("keyboard interrupt")
        break
    except Exception as e: 
        print(e)
        print(datetime.now())
        captchamultiplier*=2
        print(f"waiting {captchamultiplier} seconds...")
        time.sleep(captchamultiplier)
