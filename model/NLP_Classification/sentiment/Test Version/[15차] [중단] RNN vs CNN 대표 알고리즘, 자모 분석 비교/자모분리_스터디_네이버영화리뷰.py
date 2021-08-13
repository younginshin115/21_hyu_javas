import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import tensorflow as tf

total_data = pd.read_table('C:\\Git\\hy21-pbl-chat-analysis\\model\\Colab Notebooks\\NLP_Classification\\sentiment\\Cleaned Dataset\\clean_naver_movie_review_total_data.txt')

# okt = Okt()
# stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

# pip install jamo
#
# from jamo import h2j, j2hcj

# 문장단위 자모 파일 로드
import json
with open('C:\\Git\\hy21-pbl-chat-analysis\\model\\Colab Notebooks\\NLP_Classification\\sentiment\\Cleaned Dataset\\naver_movie_review_total_data_jamo1(sentence).json', encoding='UTF8') as json_file:
    X_train_j1 = json.load(json_file)

tokenizer_j1 = Tokenizer()
tokenizer_j1.fit_on_texts(X_train_j1)

vocab_size = 8444

tokenizer_j1 = Tokenizer(vocab_size, oov_token = 'OOV') 
tokenizer_j1.fit_on_texts(X_train_j1)
X_train_j1 = tokenizer_j1.texts_to_sequences(X_train_j1)
y_train = np.array(total_data['label'])

"""# 패딩"""
max_len = 25

"""# LSTM으로 모델 만들기"""
# 필요한 매트릭 선언, AUC-ROC, F1-Score, AUC-PR 에 필요한 지표 모두 체크
ROCauc = tf.keras.metrics.AUC(curve="ROC") # auc_1
PRauc = tf.keras.metrics.AUC(curve="PR") # auc_2
RECALL = tf.keras.metrics.Recall()
PRECISION = tf.keras.metrics.Precision()
TP = tf.keras.metrics.TruePositives()
TN = tf.keras.metrics.TrueNegatives()
FP = tf.keras.metrics.FalsePositives()
FN = tf.keras.metrics.FalseNegatives()

model = Sequential()
model.add(Embedding(vocab_size, 100))
model.add(LSTM(128))
model.add(Dense(1, activation='sigmoid'))

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
mc = ModelCheckpoint('jamo(sentence)_test.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc', ROCauc, PRauc, TP, TN, FP, FN])

history = model.fit(X_train_j1, y_train, epochs=15, callbacks=[es, mc], batch_size=30)
#
# """# 형태소단위 자모 분리"""
#
# # 형태소단위 자모 분리
# X_train_j2 = []
# for sentence in total_data['document']:
#     temp_X_j2 = okt.morphs(sentence, stem=True) # 토큰화
#     temp_X_j2 = [word for word in temp_X_j2 if not word in stopwords] # 불용어 제거
#     for word in temp_X_j2:
#         temp_X_j2 = j2hcj(h2j(word)) # 자모 분리
#     X_train_j2.append(temp_X_j2)
#
# print(len(X_train_j2))
# X_train_j2[:3]
#
# # 형태소단위 자모 저장
# import json
# json = json.dumps(X_train_j2, ensure_ascii=False)
# jamo2 = open("naver_movie_review_total_data_jamo2(tokened).json", "w", encoding="utf-8")
# jamo2 .write(json)
# jamo2 .close()
#
# # 형태소단위 자모 로드
# import json
# with open('naver_movie_review_total_data_jamo2(tokened).json', encoding='UTF8') as json_file:
#     X_train_j2 = json.load(json_file)
# print(len(X_train_j2))
# X_train_j2[:3]
#
# tokenizer_j2 = Tokenizer()
# tokenizer_j2.fit_on_texts(X_train_j2)
# print(len(tokenizer_j2.word_index))
# tokenizer_j2.word_index
#
#

