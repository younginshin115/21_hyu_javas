import json
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

loaded_model = load_model('/home/adminuser/mymodel/sentiment_model_0.1.h5')

okt = Okt()
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다'] 
max_len = 30 
tokenizer = Tokenizer()
with open('/home/adminuser/mymodel/sentiment_vocab_0.1.json') as json_file:
    vocab = json.load(json_file)
    tokenizer.word_index = vocab

def sentiment_predict(new_sentence):
    new_sentence = [word for word in new_sentence if not word in stopwords]
    #  tokenizer.fit_on_texts(new_sentence)
    encoded = tokenizer.texts_to_sequences([new_sentence])
    pad_new = pad_sequences(encoded, maxlen = max_len)
    score = float(loaded_model.predict(pad_new))
    return round(score,1)
