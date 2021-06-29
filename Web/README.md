# 가상환경 만들기

1. 파이썬 설치
1. 가상 환경을 만들 폴더 생성
```
mkdir project
cd project
```

1. 가상 환경 생성
```
python -m venv final_project
```

1. 가상 환경 진입
```
cd final_project\Scripts
activate
```

\[참고\] 가상 환경 종료
```
deactivate
```


# 필요 패키지
기본 패키지
```
pip install flask
pip install wheel
```

형태소 분석용
```
pip install JPype1-py3==0.5.5.2
pip install konlpy
```
JPype1-py3 이 오류가 생기면 Visual Studio 2017과 함께 c++ 개발자 패키지를 깔아야 한다

워드클라우드용
```
pip install wordcloud
```

youtube 크롤링용
```
pip install youtube-dl
pip install pytchat
pip install pafy
```

kafka 연결
```
pip install kafka-python
```
