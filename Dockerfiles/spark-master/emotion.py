import re
import os
import json
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
import tensorflow as tf
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

loaded_model = load_model('/spark/sentiment_model_0.1.h5') # 감성 분류


okt = Okt()
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
max_len = 30
vocab_size = 19416
tokenizer = Tokenizer(vocab_size)
with open('/spark/sentiment_vocab_0.1.json', encoding='UTF8') as json_file:
    vocab = json.load(json_file)
    tokenizer.word_index = vocab

def sentiment_predict(new_sentence):
    new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', new_sentence)
    if new_sentence == "" or new_sentence.isspace():
        return float(-1)
    else : 
        new_sentence = okt.morphs(new_sentence, stem=True)
        new_sentence = [word for word in new_sentence if not word in stopwords]
        if not new_sentence:
            return float(-1)
        else:
            encoded = tokenizer.texts_to_sequences([new_sentence])
            pad_new = pad_sequences(encoded, maxlen = max_len)
            score = loaded_model.predict(pad_new)
            return round(float(score), 2)