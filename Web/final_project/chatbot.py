from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import jsonify

import pafy
import multiprocessing as mp

import c_crawling
import c_kafka
import c_wordcloud

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'admin'
kafka_topic = "test_topic"

cc = c_crawling.c_crawling()
ck = c_kafka.c_kafka()
cwc = c_wordcloud.c_wordcloud()

@app.route('/')
def main_chatbot():
    if mp.active_children():
        for i in mp.active_children():
            i.terminate()
    return render_template('index.html')

@app.route('/chatcategory', methods=['POST'])
def chat_category():
    category_val = request.form.get('categories')
    url_val = request.form.get('searchbar')
    if url_val:
        if category_val == 'youtube':
            url_id = url_val.split("=")[1] # 주소 형태 : https://www.youtube.com/watch?v=MN1JsMbNMs0
            p = mp.Process(target=cc.youtube_to_kafka, args=(url_id, kafka_topic,))
            p.start()
            pafy.set_api_key('AIzaSyB0oN8aGAJDk5PEWpR07Tn7gN4w30fwnOI')
            v = pafy.new(url_id)
            return render_template('result.html', data_list=v.title)
        elif category_val == 'twitch':
            url_id = url_val.split("/")[-1] # 주소 형태: https://www.twitch.tv/lol_ambition
            p = mp.Process(target=cc.twitch_to_kafka, args=(url_id, kafka_topic,))
            p.start()
            return render_template('result.html', data_list=url_id+'의 방송입니다')
        elif category_val == 'afreecatv':
            return render_template('result.html', data_list='아직 구현되지 않은 기능입니다')
    else:
        flash('URL을 입력해주세요')
        return render_template('index.html')

num = 1
wordcloud_lst = ['시작']
@app.route('/update', methods=['POST'])
def update():
    global num
    consumer = ck.From_kafka(kafka_topic)
    for message in consumer:
        print({"msg": message.value})
        if message.value['noun_token']:
            wordcloud_lst.extend(message.value['noun_token'])
        if len(wordcloud_lst) > 1000:
            del wordcloud_lst[:len(wordcloud_lst) - 1000]
        cwc.woco_pic(wordcloud_lst, num, message.value['video_id'])
        num += 1
        image_name = message.value['video_id']+str(num-1)+".png"
        return jsonify({"msg":message.value, "image_name": image_name})

import logging
import datetime
from pytz import timezone

logging.basicConfig(filename="logs/chatbot.log", level=logging.DEBUG)

def log(request, message):
    log_date = get_log_date()
    log_message = "{0}/{1}/{2}".format(log_date, str(request), message)
    logging.info(log_message)

def error_log(request, error_code, error_message):
    log_date = get_log_date()
    log_message = "{0}/{1}/{2}/{3}".format(log_date, str(request), error_code, error_message)
    logging.info(log_message)

def get_log_date():
    dt = datetime.datetime.now(timezone("Asia/Seoul"))
    log_date = dt.strftime("%Y%m%d_%H:%M:%S")
    return log_date

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=False)

