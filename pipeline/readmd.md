# 사전준비
**설명이 안적힌 코드는 pyspark.ipynb를 참고**

<span style="color:blue">**1.jar파일 다운(/adminuser/home/library 위에 저장)**</span>
```
mkdir /adminuser/home/library 

wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.1.1/spark-sql-kafka-0-10_2.12-3.1.1.jar

wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.8.0/kafka-clients-2.8.0.jar

wget https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.1.1/spark-token-provider-kafka-0-10_2.12-3.1.1.jar

<너무 오래된 자료라 maven repository에 없음, 압축 파일을 다운받아서 tar 명령어로 압축을 풀고 그 안의 jar 파일을 library로 옮겨야 함>  
wget http://archive.apache.org/dist/httpcomponents/commons-httpclient/3.0/binary/commons-httpclient-3.0.1.tar.gz

```

<span style="color:blue">**2.pip install(모델링에 필요)** – pip를 local환경에 깔게되면 오류가 뜸(다른 방법을 찾으면 더 좋겠다)(/adminuser/home/library 위에 저장)**</span>

```
pip install keras 
pip install gensim
pip install scikit-learn
pip install nltk
pip install konlpy
pip install numpy
pip install matplotlib
pip install JPype1-py3==0.5.5.2
pip install tensorflow-cpu
```

<span style="color:blue">**3.모델적용 파이썬 모듈 만들기**</span>

```
mkdir /adminuser/home/mymodel
cd /adminuser/home/mymodel
vi emotion0628.py
vi abuse0628.py
```
**(emotion0628.py, abuse0628.py 파일은 따로 올려놓음)**

<span style="color:blue">**4.h5 모델,말뭉치 filezila를 통해 /adminuser/home/mymodel 파일에 넣기**</span>

<span style="color:blue">**5.checkpoint 폴더 만들기 -> 스파크가 계속 돌기 때문에 shutdown되면 메시지를 남겨줄 폴더를 만들어야함(같은 checkpoint에서 여러 번 돌리면 오류가 생기므로 새 폴더를 만들어서 해결하면 됨!)**</span>

```
mkdir /tmp/dtn/checkpoint
```


============================================      
# 사전준비 되어있으면 여기부터 실행!
============================================   

<span style="color:blue">**6.kafka 설정**</span>

(1) 주키퍼 실행 : kafka를 사용하기 위해선 zookeeper가 필요(zookeeper 위에서 돌기 때문에)
```
cd /usr/local/zookeeper/bin
sudo ./zkServer.sh start
```

(2) 카프카 실행
```
cd /usr/local/kafka/bin
./kafka-server-start.sh ../config/server.properties
```

(3) 카프카 콘솔 열기(inchat, outchat) -> 새로운 terminal 열기            
**--from-beginning : 처음에 한번만 해주면 됨(후에도 계속 치면 들어가있는거 다 나옴)**
=================================================    
kafka에서 들어오는 topic : inchat          
모델 적용된 데이터를 kafka로 보내는 topic : outchat   
=================================================      
```
cd /usr/local/kafka/bin

./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic inchat --from-beginning

./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic outchat --from-beginning
```
<span style="color:blue">**7.하둡 켜기(WRITESTREAM에서 하둡 관련 오류가 남, 하둡을 켜서 해결했음)**</span>

```
start-all.sh
```

<span style="color:blue">**8.pyspark streaming**</span>          

(1) pyspark 켜기(필요한 jar 파일들 끼워서 -> 앞에서 wget한 jar파일들)
```
pyspark --master=local[1] --jars /root/library/commons-httpclient-3.0.1.jar,/root/library/spark-sql-kafka-0-10_2.12-3.1.1.jar,/root/library/commons-pool2-2.10.0.jar,/root/library/kafka-clients-2.8.0.jar,/root/library/spark-token-provider-kafka-0-10_2.12-3.1.1.jar
```

(2) 필요한 모듈 import
```
from pyspark.sql.functions import *
from pyspark.sql.types import *
```
(3) 파일 import(h5 모델과 파이썬 모듈)       
****emotion model****

```
sc.addFile("/adminuser/home/mymodel/emotion0628.py")
import emotion0628
```

****abuse model****      

```
sc.addFile("/adminuser/home/mymodel/abuse0628.py")
import abuse0628
```
(4) readStream 사용해서 크롤링한 json 데이터를kafka(topic:inchat)을 통해 읽어오기
시작할 때 창을 보면 sparkSession을 spark로 쓸 수 있다는 기본 설정이 있다.
```
df_raw = spark \
.readStream \  
.format('kafka') \
.option('kafka.bootstrap.servers', 'localhost:9092') \           
.option("startingOffsets", "earliest") \             
.option('subscribe', 'inchat') \          
.load()         
```

<코드설명>
df_raw = spark \
.readStream \
<span style="color:purple">**#kafka 형태로**</span>  
.format('kafka') \
<span style="color:purple">**#kafka 포트 : 9092**</span> 
.option('kafka.bootstrap.servers', 'localhost:9092') \          
<span style="color:purple">**#처음부터 실행**</span> 
.option("startingOffsets", "earliest") \          
<span style="color:purple">**topic inchat에서 읽어옴**</span>           
.option('subscribe', 'inchat') \          
.load()         
