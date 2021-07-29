# 필요 프레임워크 및 라이브러리 준비
import re
import os
import json
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

# 가상환경에서 GPU사용불가로 인한 오류메시지 숨김
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'

# 전처리 및 모델 로드
# 모델 가중치 파일 로드
loaded_model = load_model('sentiment_model_0.1.h5') # 감성 분류


# 토크나이징
okt = Okt() # 형태소 분석기 객체 생성
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다'] # 불용어 정의
max_len = 30 # 패딩 길이 정의
vocab_size = 19416 #출현빈도가 높은 단어 집합 길이
tokenizer = Tokenizer(vocab_size) # 토크나이저 객체 생성
with open('sentiment_vocab_0.1.json', encoding='UTF8') as json_file:
  vocab = json.load(json_file)
  tokenizer.word_index = vocab

# 감성분석 모델 실행 함수 
def sentiment_predict(new_sentence):
  new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', new_sentence)
  # if not str 로 하면 if에서 변수가 공백 및 null값은 false로 반환하므로 비교연산자를 안써도되는데
  # 실제로는 null은 잡는데 공백은 못잡아서 그냥 비교연산자씀
  if new_sentence == "" or new_sentence.isspace():    # 공백이거나 NUll 인 경우
    return float(-1)  # 프론트에서 계산에 미포함되도록 (0-1)구간 예외값 리턴
  else :                                            # 공백이거나 NUll 인 아닌 경우
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화,   "stem =True" 어간 추출(ex 해야지 -> 하다)
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    if not new_sentence : # 불용어 제거 후 빈리스트 인 경우
      return float(-1)
    else:
      encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
      pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
      score = loaded_model.predict(pad_new) # 예측
      return round(float(score), 2)

  #코랩/주피터에서 동작 테스트 코드
  #if(score > 0.5):
  #  print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
  #else:
  #   print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))


# 로컬IDE에서 동작 테스트 코드
while True:
  new_sentence = input("리뷰를 입력하세요 ")
  score = sentiment_predict(new_sentence)
  print(score)
  if(score > 0.5):
    print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
  else:
    print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))