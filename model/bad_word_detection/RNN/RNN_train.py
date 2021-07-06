# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # 바닐라 RNN(VanillaRNN)을 이용한 비속어 분류

# ## 1. 데이터 전처리

#전처리 도구 임포트
import koco
import pandas as pd
import numpy as np
# %matplotlib inline
import matplotlib.pyplot as plt
import re
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

#데이터 로드
data = pd.read_csv("train.tsv", delimiter='\t')
print(data)

#총 샘플의 수 확인
print('총 샘플의 수 :',len(data))

#총 7,896 샘플 존재, 상위 10개 샘플 출력
data[:10]

#불필요한 열 제거|
del data['contain_gender_bias']
del data['bias']
data['hate'] = data['hate'].replace(['none','offensive','hate'],[0,1,1])
data[:5]

#data 정보 확인
data.info()

# Null 값 확인
data.isnull().values.any()

# 중복 데이터 확인
data['comments'].nunique(), data['hate'].nunique()

#중복 샘플 제거
data.drop_duplicates(subset=['comments'], inplace=True)

print('총 샘플의 수: ', len(data))

#레이블 값의 분포 시각화
data['hate'].value_counts().plot(kind='bar');

#데이터 분포 수치 확인
print(data.groupby('hate').size().reset_index(name='count'))

# X,y 분리|
X_data = data['comments']
y_data = data['hate']
print("내용의 개수 : {}".format(len(X_data)))
print("레이블의 개수: {}".format(len(y_data)))

# 케라스 토크나이저를 통해 토큰화와 정수 인코딩 과정 수행
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_data) 
sequences = tokenizer.texts_to_sequences(X_data)

print(sequences[:5])

#X_data에 존재하는 모든 단어와 부여된 인덱스 리턴, 출력 결과 확인
word_to_index = tokenizer.word_index
print(word_to_index)

# +
# 각 단어에 대한 등장 빈도수는 tokenizer.word_counts.items()를 출력 확인 가능
# 빈도수 낮은 단어들이 훈련 데이터에서 얼만큼의 비중을 차지하는지 확인 가능
# 등장 빈도수가 1회 밖에 되지 않는 단어들이 전체 단어 집합에서 얼만큼의 비율을 차지하며,
# 전체 훈련 데이터에서 등장 빈도로 얼만큼의 비율을 차지하는지 확인 가능
threshold = 2
total_cnt = len(word_to_index) # 단어의 수
rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

# 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
for key, value in tokenizer.word_counts.items():
    total_freq = total_freq + value

    # 단어의 등장 빈도수가 threshold보다 작으면
    if(value < threshold):
        rare_cnt = rare_cnt + 1
        rare_freq = rare_freq + value

print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s'%(threshold - 1, rare_cnt))
print("단어 집합(vocabulary)에서 희귀 단어의 비율:", (rare_cnt / total_cnt)*100)
print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq)*100)
# -

#등장 빈도 1회인 단어 제외 
tokenizer = Tokenizer(num_words = total_cnt - rare_cnt + 1)

#단어 집합의 크기를 vocab_size에 저장,  
#주의할 점은 패딩을 위한 토큰인 0번 단어를 고려하며 +1을 해서 저장해주어야 한다는 점
vocab_size = len(word_to_index) + 1
print('단어 집합의 크기: {}'.format((vocab_size)))



#훈련 데이터와 데스트 데이터 8:2로 분리
n_of_train = int(len(sequences) * 0.8)
n_of_test = int(len(sequences) - n_of_train)
print('훈련 데이터의 개수 :',n_of_train)
print('테스트 데이터의 개수:',n_of_test)

# X_data 정수 인코딩 결과를 X_data로 변경, 전체 데이터 길이, 길이 분포 확인
X_data = sequences
print('최대 길이 : %d' % max(len(l) for l in X_data))
print('평균 길이 : %f' % (sum(map(len, X_data))/len(X_data)))
plt.hist([len(s) for s in X_data], bins=50)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
plt.show()

#max_len보다 길이가 짧은 샘플은 숫자 0이 패딩된다.
max_len = 39
# 전체 데이터셋의 길이는 max_len으로 맞춥니다.
data = pad_sequences(X_data, maxlen = max_len)
print("훈련 데이터의 크기(shape): ", data.shape)

#X_data 크기 7896 x 39  
X_test = data[n_of_train:] 
y_test = np.array(y_data[n_of_train:]) 
X_train = data[:n_of_train] 
y_train = np.array(y_data[:n_of_train]) 

# ## 2. RNN 비속어 분류 모델 설계

from tensorflow.keras.layers import SimpleRNN, Embedding, Dense
from tensorflow.keras.models import Sequential

# +
model = Sequential()
model.add(Embedding(vocab_size, 32)) # 임베딩 벡터의 차원은 32
model.add(SimpleRNN(32)) # RNN 셀의 hidden_size는 32
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
history = model.fit(X_train, y_train, epochs=4, batch_size=64, validation_split=0.2)
# -

print("\n 테스트 정확도: %.4f" % (model.evaluate(X_test, y_test)[1]))

epochs = range(1, len(history.history['acc']) + 1)
plt.plot(epochs, history.history['loss'])
plt.plot(epochs, history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()




