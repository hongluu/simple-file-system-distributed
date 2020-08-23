FROM python:3.7
RUN pip install rpyc
RUN pip install watchdog
WORKDIR app
COPY auto_sync.py .

CMD python auto_sync.py
