# 필요 프레임워크 및 라이브러리 준비
import pandas as pd
import numpy as np
# %matplotlib inline
import matplotlib.pyplot as plt
import re
import urllib.request
import os
import json
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# 가상환경에서 GPU사용불가로 인한 오류메시지 숨김
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'

# 전처리 및 모델 로드
# 모델 가중치 파일 로드
loaded_model = load_model('slang_model_0.1.h5') # 감성 분류

# 토크나이징
okt = Okt() # 형태소 분석기 객체 생성
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다'] # 불용어 정의
max_len = 30 # 패딩 길이 정의
tokenizer = Tokenizer() # 토크나이저 객체 생성
with open('slang_vocab_0.1.json', encoding='UTF8') as json_file:
  vocab = json.load(json_file)
  tokenizer.word_index = vocab

# 학습한 모델에 새로운 예측값을 얻는 것은 model.predict() 사용
# 그리고 예측할 때에도 동일한 전처리 수행해야함.
# 감성분석 모델 실행 함수 
def slang_predict(new_sentence):
  new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
  new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화,   "stem =True" 어간 추출(ex 해야지 -> 하다)
  new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
  encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
  pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
  score = float(loaded_model.predict(pad_new)) # 예측
  # return score
  if (score > 0.5):
    print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
  else:
    print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))

# 로컬IDE에서 동작 테스트
# while True:
#   new_sentence = input("리뷰를 입력하세요 ")
#   slang_predict(new_sentence)
