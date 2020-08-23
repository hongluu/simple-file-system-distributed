FROM python:3.7
RUN pip install rpyc
WORKDIR app
COPY master.py .
COPY dfs.conf .

CMD python master.py
