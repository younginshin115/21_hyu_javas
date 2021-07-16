FROM nvidia/cuda:11.0-devel-ubuntu18.04
COPY --from=openjdk:8-alpine / /
COPY --from=python:3.9.5 / /
ARG SPARK_VERSION=3.1.2
ARG HADOOP_VERSION=3.2

COPY start-master.sh /start-master.sh
COPY start-worker.sh /start-worker.sh

RUN echo "* Installing Spark version: ${SPARK_VERSION}"
RUN echo "* Installing Hadoop version: ${HADOOP_VERSION}"

RUN apk --update add wget tar bash curl vim

RUN wget https://mirror.navercorp.com/apache/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

RUN tar -zxvf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /spark && \
rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

RUN cd /spark/jars/ &&\
    curl -O https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.8.0/kafka-clients-2.8.0.jar &&\
    curl -O https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.1.2/spark-sql-kafka-0-10_2.12-3.1.2.jar &&\ 
    curl -O https://repo1.maven.org/maven2/commons-httpclient/commons-httpclient/3.0.1/commons-httpclient-3.0.1.jar &&\
    curl -O https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.10.0/commons-pool2-2.10.0.jar &&\
    curl -O https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.1.2/spark-token-provider-kafka-0-10_2.12-3.1.2.jar &&\
    curl -O https://repo1.maven.org/maven2/org/elasticsearch/elasticsearch-spark-30_2.12/7.13.0/elasticsearch-spark-30_2.12-7.13.0.jar

ENV PYSPARK_PYTHON=python3
#ENV PYTHONPATH="/spark/python:/spark/python/lib/py4j-0.10.9-src.zip:/spark/python/lib/pyspark.zip:${PYTHONPATH}"
ENV PYTHONPATH="${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-0.10.9-src.zip:${PYTHONPATH}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends -f \
    nvidia-modprobe

ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/usr/local/cuda-11.0/lib64/stubs:/usr/local/cuda-11.0/compat

RUN chmod +x /start-master.sh
RUN chmod +x /start-worker.sh
WORKDIR /spark

COPY . /spark

RUN pip install --upgrade pip && \
pip install --no-cache-dir -r requirements.txt && \
sed -i "s|convertStrings\=True| |g" /usr/local/lib/python3.9/site-packages/konlpy/jvm.py && \
sed -i "s|)\,|)|g" /usr/local/lib/python3.9/site-packages/konlpy/jvm.py
