# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import jsonify

import pafy
import multiprocessing as mp
import os
from glob import glob

import c_crawling
import c_kafka
import c_wordcloud
import time

import re
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'admin'
CORS(app)

kafka_topic = ('inchat', 'outchat')

cc = c_crawling.c_crawling()
ck = c_kafka.c_kafka()
cwc = c_wordcloud.c_wordcloud()

@app.route('/')
def main_chatbot():
    if mp.active_children():
        for i in mp.active_children():
            i.terminate()
    time.sleep(1)
    [os.remove(f) for f in glob("./static/img/*.png")]
    global wordcloud_lst
    wordcloud_lst = ['시작']
    global replica_list
    replica_list = []
    global num
    num = 0
    return render_template('index.html')

@app.route('/chatcategory', methods=['POST'])
def chat_category():
    category_val = request.form.get('categories')
    url_val = request.form.get('searchbar')
    if url_val:
        if category_val == 'youtube':
            try:
                url_id = re.split("[=&]",url_val)[1] # 주소 형태 : https://www.youtube.com/watch?v=MN1JsMbNMs0
                p = mp.Process(target=cc.youtube_to_kafka, args=(url_id, kafka_topic[0],))
                p.start()
                pafy.set_api_key('AIzaSyB0oN8aGAJDk5PEWpR07Tn7gN4w30fwnOI')
                v = pafy.new(url_id)
                return render_template('result.html', data_list=v.title)
            except:
                flash('Youtube URL을 입력해주세요')
                return render_template('index.html')
        elif category_val == 'twitch':
            url_id = url_val.split("/")[-1] # 주소 형태: https://www.twitch.tv/lol_ambition
            if '=' in url_id:
                flash('Twitch URL을 입력해주세요')
                return render_template('index.html')
            else:
                p = mp.Process(target=cc.twitch_to_kafka, args=(url_id, kafka_topic[0],))
                p.start()
                return render_template('result.html', data_list=url_id+'의 방송입니다')
        elif category_val == 'afreecatv':
            return render_template('result.html', data_list='아직 구현되지 않은 기능입니다')
    else:
        flash('URL을 입력해주세요')
        return render_template('index.html')

num = 1
wordcloud_lst = ['시작']
replica_list = []
@app.route('/update', methods=['POST'])
@cross_origin()
def update():
    global num
    consumer = ck.From_kafka(kafka_topic[1])
    for message in consumer:
        if message.value['chat_id'] in replica_list:
            pass
        else:
            replica_list.append(message.value['chat_id'])
            wordcloud_lst.extend(message.value['noun_token'])
            if len(wordcloud_lst) > 200:
                del wordcloud_lst[:len(wordcloud_lst) - 200]
            cwc.woco_pic(wordcloud_lst, num, message.value['video_id'])
            num += 1
            image_name = message.value['video_id'] + "_" + str(num - 5).zfill(4) + ".png"
            print({"msg": message.value})
            return jsonify({"msg": message.value, "image_name": image_name})

import logging.config
import yaml
from concurrent_log_handler import ConcurrentRotatingFileHandler

loggingConfigPath = 'logging.yaml'
if os.path.exists(loggingConfigPath):
    with open(loggingConfigPath, 'rt') as f:
        loggingConfig = yaml.safe_load(f.read())
        logging.config.dictConfig(loggingConfig)
else:
    logging.basicConfig(level=logging.INFO)

logging.getLogger(__name__)

logging.debug("debug")
logging.info("info")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=False)

