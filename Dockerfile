FROM python3
RUN pip install -r requirement.txt
ADD coin-main.py /app
CMD [ "python3", "./app/coin-main.py" ]
