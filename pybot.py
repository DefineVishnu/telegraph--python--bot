# -*- coding: utf-8 -*-
#"""
#Created on Sat Mar 17 08:15:35 2018
#
#@author: vishnu.kv
#"""
#
#import json
#import requests
#import time
#import urllib
#
#from dbHelper import DBHelper
#
#TOKEN = '495947458:AAHw7oJJGZRgOpvXj40zPjK5m_uF6iT-PyM'
#URL = "https://api.telegram.org/bot{}/".format(TOKEN)
#
#db=DBHelper()
#def get_url(url):
#    try:
#        response = requests.get(url)
#        content = response.content.decode("utf8")
#        return content
#    except Exception as e:
#        print(e)
#
#
#def get_json_from_url(url):
#    content = get_url(url)
#    js = json.loads(content)
#    return js
#
#
#def get_updates(offset=None):
#    url = URL + "getUpdates"
#    if offset:
#        url += "?offset={}".format(offset)
#    js = get_json_from_url(url)
#    return js
#
#
#def get_last_update_id(updates):
#    update_ids = []
#    for update in updates["result"]:
#        update_ids.append(int(update["update_id"]))
#    return max(update_ids)


# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 08:15:35 2018

@author: vishnu.kv
"""

import json
import requests
import time
import urllib

from dbHelper import DBHelper

TOKEN = '495947458:AAHw7oJJGZRgOpvXj40zPjK5m_uF6iT-PyM'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

db=DBHelper()
def get_url(url):
    try:
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content
    except Exception as e:
        print(e)


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def handleUpdates(updates):
    for update in updates['result']:
        
        try:
#            print(update)
            text=update['message']['text']
            chat=update['message']['chat']['id']
            items=db.get_items()
            
            if text == "/done":
                keyboard = buildKeyBord(items)
                send_message("Select an item to delete", chat, keyboard)
            elif text == "/start":
                send_message("Welcome to your personal To Do list. Send any text to me and I'll store it as an item. Send /done to remove items", chat)
            if text in items:
                db.deleteItems(text)
                items=db.get_items()
                keyboard = buildKeyBord(items)
                send_message("Select an item to delete", chat, keyboard)
            
            elif text.startswith("/"):
                    continue
            else:
                db.addItems(text)
                items=db.get_items()
            message="\n".join(items)
            send_message(message,chat)
        except KeyError as e:
            print(e)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id,replyMarkup=None):
    print('////////////////////////////////////////////////')
    print('send')
    print('text {}'.format(text))
    print('chat_id {}'.format(chat_id))
    print('replyMarkup {}'.format(replyMarkup))

    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if replyMarkup:
        url += "&reply_markup={}".format(replyMarkup)
    print(url)
    get_url(url)


def main():
    last_update_id = None
    print('started')
    while True:
        updates = get_updates(last_update_id)
#        print(updates)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handleUpdates(updates)
        time.sleep(1)

def buildKeyBord(items):
    keybord=[[item] for item in items]
    replyMarkup={"keyboard":keybord, "one_time_keyboard": True}
#    print(replyMarkup)
    return json.dumps(replyMarkup)



#def get_last_chat_id_and_text(updates):
#    num_updates = len(updates["result"])
#    last_update = num_updates - 1
#    text = updates["result"][last_update]["message"]["text"]
#    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
#    return (text, chat_id)










if __name__ == '__main__':
    main()
