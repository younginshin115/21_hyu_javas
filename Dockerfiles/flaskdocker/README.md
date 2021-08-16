# Description
ML기반 챗봇 "JAVAS" 가동에 필요한 Flask container 빌드 디렉토리

<br>

# Directories

|디렉토리명|소개|
|:---|:---|
|logs|Flask 가동시 log가 기록되는 디렉토리|
|static|Flask에서 사용하는 자원이 저장된 디렉토리|
||css : Flask에서 사용하는 css 파일이 저장된 디렉토리|
||font :Flask에서 사용하는 폰트가 저장된 디렉토리|
||img : 서비스가 작동하는 동안 워드 클라우드 이미지를 저장해두는 임시 디렉토리|
||js : Flask에서 사용하는 JavaScript 파일이 저장된 디렉토리|
||contact_icon.png : 문의하기 버튼 아이콘 이미지|
||dashboard_icon.png : 대시보드 버튼 아이콘 이미지|
||home_icon.png : 홈 버튼 아이콘 이미지|
||logo_new.png : 인덱스 페이지에 표시되는 로고 이미지|
||logo_new_white.png : 결과 페이지에 표시되는 흰색 로고 이미지|
||wordcloud.png : 워드클라우드가 작동하기 전에 뜨는 임시 이미지|
|templates|Flask에서 사용하는 html 파일이 저장된 디렉토리|
||index.html : 영상의 채널과 URL을 입력하는 index 페이지|
||layout.html : header와 footer를 포함한 layout 페이지|
||result.html : 채팅과 워드 클라우드, 감정 대시보드 등 서비스가 제공되는 페이지|
|app.py|Flask가 작동하는 main 파일|
|c_crawling.py|크롤링 모듈|
|c_kafka.py|카프카 연결 모듈|
|c_token.py|형태소 분석 모듈|
|c_wordcloud.py|워드클라우드 생성 모듈|
|Dockerfile|Flask 컨테이너 빌드 파일|
|logging.yaml|logging 설정 파일|
|requirements.txt|Flask 실행시 필요한 패키지 리스트|
|uwsgi.ini|uwsgi 설정 파일|