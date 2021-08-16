# Description

## 프로젝트 개요
라이브 커머스 방송을 원활하게 진행할 수 있도록 보조하는 머신러닝 기반 챗봇 'JAVAS' 개발

## 프로젝트 기간
2021.06.07~2021.8.17

## 주요 기능
- 다양한 라이브커머스 채널 지원(유튜브, 트위치, 네이버 쇼핑라이브) 

- 채팅 텍스트를 머신러닝으로 분석하여 비속어 필터링 

- 채팅창의 긍/부정 감정 분석 및 시각화 

- 채팅창의 트렌드를 파악하기 위해 실시간 빈도순 워드 클라우드 제공 

## 프로젝트 팀 인원 : 총 6명
### 팀내 역할
- 역할 1 프로젝트 전체 관리 및 최종 발표

- 역할 2 Docker를 사용하여 총 18개 서비스, 21개 컨테이너로 구성된 데이터 실시간 플랫폼 구성

- 역할 3 웹개발(서버, 클라이언트)

  - 이용자가 라이브 방송 채널을 선택하고 URL을 입력하면 해당 방송의 채팅을 실시간으로 스크레이핑하여 Kafka로 전송하는 기능 개발
  
  - Ajax로 실시간 채팅 뷰어와 워드클라우드 기능 개발, Highchart로 실시간 그래프 클라이언트에 표시, iframe으로 Grafana 대시보드를 클라이언트에 표시, emailJS로 문의메일 보내는 기능 개발
  
  - Python의 Multiprocessing으로 웹서비스를 담당하는 메인 프로세스와 채팅 메시지 스크레이핑 후 Kafka에 데이터를 전송하는 차일드 프로세스, Kafka에서 데이터를 수신 받아 웹에 표시하는 차일드 프로세스, 총 세가지 프로세스로 구성된 비동기 프로세스 환경 구성

## 프로젝트 결과
https://youtu.be/HLQBYAj-eO0

<br>

# Environment

|분류|이름|버전|
|:---|:---|:---|
|운영체제|ubuntu|18.04|
||Docker|20.10.7|
||Docker-compose|3.2|
||Nvidia Driver|470.57.02|
||CUDA|11.2.2|
||cuDNN|8|
|개발언어|Java|1.8|
||Python|Spark Container - 3.8.3<br>Flask Container - 3.9.5|
||Scala|2.12|
|DB|MongoDB|4.4.6|
||InfluxDB|1.8.6|
|파이프라인|Kafka|2.8.0|
||Spark|3.1.2|
||Hadoop|3.2|
||Airflow|2.1.2|
||Flink|1.13.1|
||Logstash|7.13.0|
||Elasticsearch|7.13.0|
||Grafana|8.0.6|
||Graphite|1.1.8|
||Burrow|11.1|
||Telegraf|1.19.1|
|Web|Nginx|1.14.0|
||uWSGI|2.0.19|
||Flask|2.0.1|
|ML|Tensorflow|2.5.0|
||Keras|2.4.3|
||NLTK|2.6.2|
||KoNLPy|0.5.2|
|협업툴|GitLab, OneDrive,<br>Slack, OneNote||

<br>

# Directories
|디렉토리명|소개|
|:---|:---|
|airflowdocker|Airflow 컨테이너 빌드 관련 디렉토리|
|burrowdocker|Burrow 컨테이너 빌드 관련 디렉토리, git clone한 것|
|dags|Airflow 컨테이너의 /opt/bitnami/airflow/dags 디렉토리와 volume 옵션으로 연결해놓은 폴더로 Airflow의 dags 설정 파일이 저장된 디렉토리|
|elasticsearch|Elasticsearch 컨테이너 빌드 관련 디렉토리<br>config : Elasticsearch 컨테이너의 /usr/share/elasticsearch/config 디렉토리와 volume 설정으로 연결된 디렉토리로 설정 파일이 저장된 디렉토리|
|flaskdocker|Flask 컨테이너 빌드 관련 디렉토리<br>해당 디렉토리 README.md 참조|
|flink_lib|Flink 컨테이너의 /opt/flink/usrlib 디렉토리와 volume 옵션으로 연결된 디렉토리로 Flink에서 사용하는 jar 파일이 저장된 디렉토리|
|grafana_data|Grafana 컨테이너의 /var/lib/grafana 디렉토리와 volume 옵션으로 연결된 디렉토리로 Grafana 실행에 필요한 데이터들이 저장되며 plugins 폴더만 제출|
|kafkadocker|Kafka 컨테이너 빌드 관련 디렉토리|
|logstash|Logstash 컨테이너 빌드 관련 디렉토리<br>config: Logstash 컨테이너의 /usr/share/logstash/config 디렉토리와 volume 옵션으로 연결된 디렉토리로 Logstash 설정 파일이 저장된 디렉토리<br>pipeline : Logstash 컨테이너의 /usr/share/logstash/pipeline 디렉토리와 volume 옵션으로 연결된 디렉토리로 수집용 설정 파일이 저장된 디렉토리|
|nginxdocker|Nginx 컨테이너 빌드 관련 디렉토리|
|spark-master|Spark 컨테이너 빌드 관련 디렉토리|
|telegrafdocker|Telegraf 컨테이너의 /etc/telegraf/telegraf.conf 디렉토리와 volume 옵션으로 연결된 디렉토리로 Telegraf 설정 파일이 저장된 디렉토리|
|docker-compose.yml|Docker-compose 설정 파일|
|grafana|Grafana Dashboard json 파일이 저장된 디렉토리|

<br>

# Usage

## 사용하기 전에
1. 설명(https://developers.google.com/youtube/v3/live/registering_an_application)에 따라 Youtube Livestreaming API를 발급받아 /Dockerfiles/flaskdocker/c_crawling.py 20번째 줄에 있는 {youtube_api_key}에 입력 후 저장한다.

2. 설명(https://dev.twitch.tv/docs/authentication/getting-tokens-oauth)에 따라 Twitch Token을 발급받아 /Dockerfiles/flaskdocker/c_crawling.py 46번째 줄에 있는 {twitch_token}에 입력 후 저장한다.

3. /Dockerfiles/flaskdocker/c_crawling.py 47번째 줄에 있는 {user_name}에 Twitch ID를 입력 후 저장한다.

<br>

## Ubuntu에서 컨테이너 실행
1. docker-compose.yml 파일이 있는 Dockerfiles 디렉토리로 이동

2. 아래 명령어를 입력하면 docker-compose 개발 환경 실행
```
docker-compose up -d
```

3. 아래 명령어로 컨테이너 이름 확인
```
docker ps -a
```

4. 아래 명령어로 원하는 컨테이너 접속
```
docker exec -it [컨테이너 이름 또는 아이디] /bin/bash
```
<br>

## 윈도우 환경에서 컨테이너 실행
1. WSL2 설치(참고 링크: https://www.44bits.io/ko/post/wsl2-install-and-basic-usage)

2. 윈도우에 Docker Desktop 설치(설치 링크: https://www.docker.com/products/docker-desktop)

3. Vivual Studio Code 설치 후 Docker Extension 설치

4. 터미널에서 아래 명령어를 실행하여 도커가 제대로 설치되었는 지 확인
```
docker version
```

5. 터미널에서 docker-compose.yml 파일이 있는 Dockerfiles 디렉토리로 이동

6. 아래 명령어를 입력하면 docker-compose 개발 환경 실행
```
docker-compose up -d
```

7. 아래 명령어로 컨테이너 이름 확인
```
docker ps -a
```

8. 아래 명령어로 원하는 컨테이너 접속
```
docker exec -it [컨테이너 이름 또는 아이디] /bin/bash
```

<br><br>

## 컨테이너가 실행되어있을 경우 서비스 실행

1. 아래 명령어로 spark 컨테이너에 submit을 한다.
```
docker exec -it spark-master /spark/bin/spark-submit \
--master spark://spark-master:7077 \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 \
--files /spark/metrics.properties \
--conf spark.metrics.conf=/spark/metrics.properties \
/spark/streamingspark.py
```

2. IP:5307로 접속한다(포트가 열려있지 않은 경우 포트 열어주기)

3. 원하는 채널과 URL을 입력하여 서비스를 실행한다

## 모니터링을 원하는 경우
1. 도커를 swarm 모드로 변경한다
```
docker swarm init
```

2. docker-compose up을 실행한다
```
docker-compose up -d
```

## 서버 종료
아래 명령어로 서버를 종료한다
```
docker-compose down
```