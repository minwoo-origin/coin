FROM python:3.8-slim-buster

RUN mkdir -p /app

ADD requirement.txt /app/requirement.txt
RUN pip install -r /app/requirement.txt

ADD coin-main.py /app/coin-main.py
ADD init.sh /app/init.sh



#ENTRYPOINT ["/bin/bash/", "/app/init.sh"]
