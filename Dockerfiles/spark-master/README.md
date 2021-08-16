
# Description
ML기반 챗봇 "JAVAS" 가동에 필요한 Spark container 빌드 디렉토리

<br>

# Directories

|디렉토리명|소개|
|:---|:---|
|abuse_model_v1.0.h5|비속어 탐지용 가중치 파일|
|abuse_model_v1.py|Spark streaming에 import하여 사용하는 모듈로 비속어 탐지를 위한 데이터 전처리 및 모델 적용을 담당하는 모듈|
|abuse_vocab_v1.0.json|비속어 탐지용 단어집합|
|Dockerfile|Spark 컨테이너 빌드 파일|
|metrics.properties|Spark Metrics 설정 파일|
|requirements.txt|Spark streaming 실행 시 필요한 패키지 리스트|
|sentiment_indexed_vocab_v2.0.json|감정 분석용 단어집합|
|sentiment_model_v2.0.h5|감정 분석용 가중치 파일|
|sentiment_model_v2.py|Spark streaming에 import하여 사용하는 모듈로 감정 분석을 위한 데이터 전처리 및 모델 적용을 담당하는 모듈|
|start-master.sh|Spark master를 가동시키는 쉘스크립트|
|start-worker.sh|Spark worker를 가동시키는 쉘스크립트|
|streamingspark.py|Spark Submit을 통해 Spark streaming을 실행하는 파일|
