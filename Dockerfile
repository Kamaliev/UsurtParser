FROM python:3.9-buster

ENV TZ="Asia/Yekaterinburg"
WORKDIR /UsurtApp/parser


COPY requirements.txt /UsurtApp/parser/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /UsurtApp/parser/requirements.txt

COPY ./ /UsurtApp/parser

CMD ["python", "/UsurtApp/parser/main.py"]