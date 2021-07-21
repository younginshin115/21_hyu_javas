# -*- coding: utf-8 -*-

from pytchat import LiveChat
import pafy

import socket
import re
from datetime import datetime as dt

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import c_kafka
import c_token

ck = c_kafka.c_kafka()

class c_crawling():
    def youtube_to_kafka(self, url_id, topic):
        pafy.set_api_key('AIzaSyB0oN8aGAJDk5PEWpR07Tn7gN4w30fwnOI')

        num = 0
        chat = LiveChat(video_id=url_id, topchat_only='FALSE', interruptable=False)
        while chat.is_alive():
            try:
                data = chat.get()
                items = data.items
                for c in items:
                    d = self.c_json(url_id, c.author.name, num, c.message, c.datetime)
                    num += 1
                    ck.To_kafka(topic, d)
            except KeyboardInterrupt:
                chat.terminate()
                break

    def twitch_to_kafka(self, url_id, topic):
        sock = socket.socket()

        count = 0
        num = 0

        port = 6667
        server = 'irc.chat.twitch.tv'
        sock.connect((server, port))

        token = 'oauth:snc65htpml9l2qxx3qfb75qqqe1swm'
        nickname = 'deokki9880'
        channel = "#"+url_id

        sock.send(f"PASS {token}\n".encode('utf-8'))
        sock.send(f"NICK {nickname}\n".encode('utf-8'))
        sock.send(f"JOIN {channel}\n".encode('utf-8'))

        resp = sock.recv(4096).decode('utf-8', 'ignore')
        while True:
            c_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
            minute = int(c_time.split(':')[1])
            if minute % 10 == 0:
                if count == 0:
                    print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
                    count+=1
                else:
                    resp = sock.recv(4096).decode('utf-8','ignore')
            else:
                resp = sock.recv(4096).decode('utf-8','ignore')
                count = 0

            test = resp.split('\n')

            if '' in test:
                test.remove('')
            for i in test:
                temp = re.search('@[^\r]+\r', i)
                if temp == None:
                    continue
                elif temp.group == '':
                    continue
                else:
                    text_list = re.findall("\ :[^\r]+\r", i)
                    id_list = re.findall('@[^.]+.', i)
                    if len(text_list) == 0 or len(id_list) == 0:
                        continue
                    text_list = text_list[0].replace(' :', '').rstrip()
                    id_list = id_list[0].replace('@', '').replace('.', '')
                d = self.c_json(url_id, id_list, num, text_list, c_time)
                ck.To_kafka(topic, d)
                num += 1

    def n_shoppinglive_to_kafka(self, url_id, topic):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--user-data-dir=/data")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        num = 0
        url = 'https://shoppinglive.naver.com/lives/' + url_id

        try:
            driver.get(url)
            pop_list = []
            while True:
                n_chat_id = driver.find_elements_by_class_name('Comment_id_3pR4u')
                n_chat_text = driver.find_elements_by_class_name('Comment_comment_2d0tc')
                for i in range(len(n_chat_text)):
                    c_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
                    try:
                        if n_chat_id[i].text:
                            chat_text = (n_chat_id[i].text, n_chat_text[i].text)
                            if chat_text in pop_list:
                                pass
                            else:
                                pop_list.append(chat_text)
                                d = self.c_json(url_id, n_chat_id[i].text, num, n_chat_text[i].text, c_time)
                                ck.To_kafka(topic, d)
                                num += 1
                    except:
                        pass
        finally:
            driver.quit()


    def c_json(self, video_id, user_name, chat_id, chat_text, chat_time):
        ct = c_token.c_token()

        tmp_json = {
            "video_id": video_id,
            "user_name": user_name,
            "chat_id": chat_id,
            "chat_text": chat_text,
            "noun_token": ct.noun_tokenize(chat_text),
            "chat_time": chat_time
        }
        return tmp_json