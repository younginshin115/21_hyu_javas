FROM openjdk:8
COPY --from=python:3.9.5 / /

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development

RUN mkdir -p /home/project/final_project
COPY . /home/project/final_project
WORKDIR /home/project/final_project
COPY requirements.txt /home/project/final_project

RUN pip install --upgrade pip && \
pip install wheel && \
pip install flask && \
pip install --no-cache-dir -r requirements.txt && \
sed -i "s|convertStrings\=True| |g" /usr/local/lib/python3.9/site-packages/konlpy/jvm.py && \
sed -i "s|)\,|)|g" /usr/local/lib/python3.9/site-packages/konlpy/jvm.py

EXPOSE 5005

CMD ["uwsgi", "uwsgi.ini"]
