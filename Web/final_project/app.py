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
import datetime
from pytz import timezone

import re
from flask_cors import CORS
from flask_cors import cross_origin

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'admin'
CORS(app)

kafka_topic = ('inchat', 'outchat')

cc = c_crawling.c_crawling()
ck = c_kafka.c_kafka()
cwc = c_wordcloud.c_wordcloud()

@app.route('/')
def main_chatbot():
    time.sleep(1)
    if mp.active_children():
        for i in mp.active_children():
            i.terminate()
    try:
        [os.remove(f) for f in glob("./static/img/*.png")]
    except:
        time.sleep(2)
        [os.remove(f) for f in glob("./static/img/*.png")]

    global wordcloud_lst
    wordcloud_lst = ['시작']
    global num
    num = 0
    return render_template('index.html')

@app.route('/chatcategory', methods=['POST'])
def chat_category():
    category_val = request.form.get('sources')
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
        elif category_val == 'n_shoppinglive':
            url_lst = url_val.split("/") # 주소형태: https://shoppinglive.naver.com/lives/177021
            url_id = url_lst[-1]
            if 'lives' in url_lst:
                options = webdriver.ChromeOptions()
                options.add_argument("headless")
                driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
                try:
                    driver.get(url_val)
                    n_title_val = driver.find_element_by_class_name('LiveHeader_text_2XGaZ')
                    n_title = n_title_val.text
                finally:
                    driver.close()
                p = mp.Process(target=cc.n_shoppinglive_to_kafka, args=(url_id, kafka_topic[0],))
                p.start()
                return render_template('result.html', data_list=n_title)
            else:
                flash('네이버 쇼핑라이브 URL을 입력해주세요')
                return render_template('index.html')
    else:
        flash('URL을 입력해주세요')
        return render_template('index.html')

num = 1
wordcloud_lst = ['시작']
@app.route('/update', methods=['POST'])
@cross_origin()
def update():
    global num
    consumer = ck.From_kafka(kafka_topic[1])
    for message in consumer:
        wordcloud_lst.extend(message.value['noun_token'])
        if len(wordcloud_lst) > 200:
            del wordcloud_lst[:len(wordcloud_lst) - 200]
        cwc.woco_pic(wordcloud_lst, num, message.value['video_id'])
        num += 1
        image_name = message.value['video_id'] + "_" + str(num - 5).zfill(4) + ".png"
        print({"msg": message.value})
        time_data = datetime.datetime.now(timezone('Asia/Seoul')).astimezone().timestamp() * 1000
        return jsonify({"msg": message.value, "image_name": image_name, "time_data": time_data})

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

