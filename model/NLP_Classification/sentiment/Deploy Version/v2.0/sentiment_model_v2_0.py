import re, os, json
from konlpy.tag import Mecab
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

os.environ['TF_CPP_MIN_LOG_LEVEL']='3'

import tensorflow as tf
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

loaded_model = load_model('sentiment_model_v2.0.h5')

mecab = Mecab()
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
vocab_size = 8117 
max_len = 40 
tokenizer = Tokenizer(vocab_size, oov_token ='OOV')


with open('sentiment_indexed_vocab_v2.0.json', encoding='UTF8') as json_file:
    tokenizer.word_index = json.load(json_file)

def sentiment_preprocessing(new_sentence):
    new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', new_sentence)
    if not new_sentence or new_sentence.isspace():
        return -1
    else :
        new_sentence = mecab.morphs(new_sentence)
        new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    
    if not new_sentence :
        return -1
    else:
        encoded = tokenizer.texts_to_sequences([new_sentence])
        encoded = [list(filter(bool, encoded[0]))]
        padded = pad_sequences(encoded, maxlen = max_len)
        return padded

def sentiment_predict(padded_sentence):
    score = loaded_model.predict(padded_sentence)
    return float(score)

def sentiment_model(new_sentence):
    padded_sentence = sentiment_preprocessing(new_sentence)
    if isinstance(padded_sentence, int) :
        score = float(-1)
    else :
        score = sentiment_predict(padded_sentence)
    return score