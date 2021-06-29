FROM openjdk:8-alpine  ==> FROM은 배이스 이미지를 지정한다. 반드시 지정해야 하고 태그는 될 수 있으면 구체적인 버전을 명시하는 것이
                           좋다. 다양한 배이스 이미지는 Docker hub에서 확인할 수 있다.
ARG SPARK_VERSION=3.0.3   ==> 파라미터 설정.. 코딩에서 상수로 설정해놓고 사용하는 원리이다..
ARG HADOOP_VERSION=2.7

COPY start-master.sh /start-master.sh  ==> COPY는 파일이나 디렉토리를 이미지로 복사한다. 보통은 소스를 복사하는데 쓰고, 여기서는
                                           쉘스크립트 파일을 복사하고 있다.
COPY start-worker.sh /start-worker.sh

RUN echo "* Installing Spark version: ${SPARK_VERSION}"    ==> RUN은 가장 많이 사용하는 구문이고 적혀진 명령어를 그대로 실행한다.
RUN echo "* Installing Hadoop version: ${HADOOP_VERSION}"

RUN apk --update add wget tar bash curl python3 ==>apk는 알파인 리눅스의 패키지 인스톨러이다.. 도커를 쓰면 굉장히 많이 쓰인다고한다..
RUN wget https://mirror.navercorp.com/apache/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

RUN tar -zxvf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /spark && \
rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

RUN cd /spark/jars/ &&\
    curl -O https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.8.0/kafka-clients-2.8.0.jar &&\
    curl -O https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.0.3/spark-sql-kafka-0-10_2.12-3.0.3.jar &&\
    curl -O https://repo1.maven.org/maven2/commons-httpclient/commons-httpclient/3.0.1/commons-httpclient-3.0.1.jar &&\
    curl -O https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.10.0/commons-pool2-2.10.0.jar &&\
    curl -O https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.0.3/spark-token-provider-kafka-0-10_2.12-3.0.3.jar
    ==> -O옵션은 file을 저장할 때 remote의 파일 이름으로 저장하게 해주는 옵션이다.. 매우 편리하다..
ENV PYSPARK_PYTHON=python3   ==> ENV는 환경변수를 설정하는 명령어이다.
#ENV PYTHONPATH="/spark/python:/spark/python/lib/py4j-0.10.9-src.zip:/spark/python/lib/pyspark.zip:${PYTHONPATH}"
ENV PYTHONPATH="${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-0.10.9-src.zip:${PYTHONPATH}"

RUN chmod +x /start-master.sh
RUN chmod +x /start-worker.sh

WORKDIR /spark      ==> WORKDIR은 작업 디렉토리를 설정하는 명령어이다.

