#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging
import datetime
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import os


update_id = None
access=False   

def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot("<bot id>")

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1

def shell(p, update):
    ppp=p.split(" ")
        if ppp[0]=="cd":
            os.chdir(ppp[1])
        try:
            update.message.reply_text(os.popen(p).read())
        except Exception:
            pass


def echo(bot):
    global update_id
    global access
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        p=update.message.text
        ppp=update.message.chat.username
        kkk=False
        if ppp=="<username>":
            kkk=True		
        if "/login" in p:
            pp=p.split(" ")[1]
            if pp=="VerySecretPassword123":
                access=True
                update.message.reply_text("Logged In")
            else:
                update.message.reply_text("Wrong Password")
        if p=="/logout":
            access=False
            update.message.reply_text("Logged Out")
        if access==True and kkk==True:
            shell(p,update)
        else:
            update.message.reply_text("No Access")
        






if __name__ == '__main__':
    main()
