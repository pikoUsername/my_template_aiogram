FROM python:3.8

RUN pip install -r ./requirements.txt

CMD python3 -m app
