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

# ## 1D CNN으로 dataset(일베_비속어_데이터셋을 활용한) 모델

# ### 1. 데이터 전처리

#전처리 도구 임포트
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

#데이터 로드
data = pd.read_csv('dataset.txt', sep ='|',header=None,names=['comments','label'])

#총 샘플의 수 확인
print('총 샘플의 수 :',len(data))

#총 5,825 샘플 존재, 상위 5개 샘플 출력
data[:5]

#데이터 중복 확인
data['comments'].nunique(), data['label'].nunique()

#중복 샘플 제거
data.drop_duplicates(subset=['comments'], inplace=True) # comments 열에서 중복인 내용이 있다면 중복 제거
print('총 샘플의 수 :',len(data))

#레이블 값의 분포 시각화
data['label'].value_counts().plot(kind='bar');

#수치로 확인
print(data.groupby('label').size().reset_index(name='count'))

#X와 y를 분리
X_data = data['comments']
y_data = data['label']
print('본문의 개수: {}'.format(len(X_data)))
print('레이블의 개수: {}'.format(len(y_data)))

#단어의 개수를 2,000개로 제한하고 정수 인코딩 진행
vocab_size = 2000
tokenizer = Tokenizer(num_words = vocab_size)
tokenizer.fit_on_texts(X_data) # 5825개의 행을 가진 X의 각 행에 토큰화를 수행
sequences = tokenizer.texts_to_sequences(X_data) # 단어를 숫자값, 인덱스로 변환하여 저장

#상위 10개의 생플 출력
print(sequences[:10])

#훈련 데이터와 테스트 데이터의 분리 비율 , 8:2
n_of_train = int(len(sequences) * 0.8)
n_of_test = int(len(sequences) - n_of_train)
print('훈련 데이터의 개수 :',n_of_train)
print('테스트 데이터의 개수:',n_of_test)

#전체 데이터의 가장 길이가 긴 문장과, 전체 데이터의 길이 분포 시각화
X_data = sequences
print('메일의 최대 길이 : %d' % max(len(l) for l in X_data))
print('메일의 평균 길이 : %f' % (sum(map(len, X_data))/len(X_data)))
plt.hist([len(s) for s in X_data], bins=50)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
plt.show()

# 전체 데이터셋의 길이는 max_len으로 맞춥니다.
max_len = 216
data = pad_sequences(X_data, maxlen = max_len)
print("훈련 데이터의 크기(shape): ", data.shape)

#X_data 데이터는 5825 x 216의 크기, X_train과 X_test 분리
X_test = data[n_of_train:] #X_data 데이터 중에서 뒤의 1034개의 데이터만 저장
y_test = np.array(y_data[n_of_train:]) #y_data 데이터 중에서 뒤의 1034개의 데이터만 저장
X_train = data[:n_of_train] #X_data 데이터 중에서 앞의 4135개의 데이터만 저장
y_train = np.array(y_data[:n_of_train]) #y_data 데이터 중에서 앞의 4135개의 데이터만 저장
print("훈련용 데이터의 크기(shape): ", X_train.shape)
print("테스트용 데이터의 크기(shape): ", X_test.shape)
print("훈련용 레이블의 크기(shape): ", y_train.shape)
print("테스트용 레이블의 크기(shape): ", y_test.shape)

# ### 2.1D CNN 비속어 분류하기

from tensorflow.keras.layers import Dense, Conv1D, GlobalMaxPooling1D, Embedding, Dropout, MaxPooling1D
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

model = Sequential()
model.add(Embedding(vocab_size, 32))
model.add(Dropout(0.2))
model.add(Conv1D(32, 5, strides=1, padding='valid', activation='relu'))
model.add(GlobalMaxPooling1D())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
model.summary()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])

es = EarlyStopping(monitor = 'val_loss', mode = 'min', verbose = 1, patience = 3)
mc = ModelCheckpoint('1DCNN_dataset_model.h5', monitor = 'val_acc', mode = 'max', verbose = 1, save_best_only = True)

history = model.fit(X_train, y_train, epochs = 10, batch_size=64, validation_split=0.2, callbacks=[es, mc])

print("\n 테스트 정확도: %.4f" % (model.evaluate(X_test, y_test)[1]))
