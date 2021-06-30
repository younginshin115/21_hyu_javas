version: "3.2"           ==> Docker Compose 규격의 버전을 나타낸다.

services:                ==> 서비스는 독립된 컨테이너에서 돌아가는 애플리케이션의 
                             구성 요소라고 생각하면 좋을 것 같다.. 프로젝트에서 개발하고
                             있는 애플리케이션 자체가 서비스가 될 것이고, 애플리케이션이
                             의존하는 데이터베이스도 서비스가 될 수 있다.
                             즉, 애플리케이션 뿐만 아니라 정상적으로 구동되기 위해서 필요한
                             기반 시스템까지 설정한다고 보면 된다. 그래서 로컬에 별도로
                             데이터베이스를 셋업하는 등의 추가작업이 필요없다.

  spark-master:          ==> 이미지명        

    image: merolhack/spark:latest  ==> 이미지:태그명
    container_name: spark-master
    hostname: spark-master
    build:
      context: . ==> build context를 읽어 들입니다. build context는 이미지를 
                             생성하는 데 필요한 각종 파일, 소스코드, 메타데이터 등을  
                             담고 있는 디렉터리를 의미합니다. build 명령어 제일 마지막에 
                             폴더위치 이다. 
                             빌드 컨텍스트는 이미지에 파일을 추가할 때 사용됩니다.
      dockerfile: Dockerfile  ==>파일명이 Dockerfile이 아니거나 다른 곳에 있을 때
                                 지정해줄 수 있다.
    ports:      ==> 외부로 노출시킬 포트의 맵핑을 명시한다. 호스트 외부:컨테이너 내부
      - "8080:8080"
      - "7077:7077"
    environment:    ==> 환경변수를 설정하기 위해서 사용된다.
      - "SPARK_LOCAL_IP=spark-master"
      - "SPARK_MASTER_PORT=7077"
      - "SPARK_MASTER_WEBUI_PORT=8080"
    command: "/start-master.sh"    ==> 해당 서비스가 올라올 때 해당 이미지 Dockerfile
                                       의 CMD 명령문을 무시하고 실행할 명령어를 설정하기
                                       위해서 사용된다.
  
  spark-worker:
    image: merolhack/spark:latest
    depends_on:     ==> 서비스 간의 의존 관계를 지정한다. 마스터가 생기고 워커가
                        생겨야 하기 때문에 의존 관계를 설정했다.
      - spark-master
    ports:
      - 8080
    environment:
      - "SPARK_MASTER=spark://spark-master:7077"
      - "SPARK_WORKER_WEBUI_PORT=8080"
    command: "/start-worker.sh"

  kafka:
    image: kafka:latest
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_CREATE_TOPICS: "test123:1:1"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock   ==> 볼륨 설정항목이다. 마운트가 필요한
                                                        호스트의 경로와 컨테이너의 경로를 명시해주면 
                                                        된다.
