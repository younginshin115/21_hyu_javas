FROM openjdk:8
COPY --from=python:3.9.5 / /

RUN mkdir -p /home/project/dash_app
WORKDIR /home/project/dash_app

COPY requirements.txt /home/project/dash_app
WORKDIR /home/project/dash_app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN sed -i "s|convertStrings\=True| |g" /usr/local/lib/python3.9/site-packages/konlpy/jvm.py
RUN sed -i "s|)\,|)|g" /usr/local/lib/python3.9/site-packages/konlpy/jvm.py


COPY . /home/project/dash_app

WORKDIR /home/project/dash_app/final_project

RUN python3 -m venv venv
RUN . venv/bin/activate
RUN export FLASK_APP=chatbot && \
export FLASK_ENV=development && \
flask run --host 0.0.0.0
