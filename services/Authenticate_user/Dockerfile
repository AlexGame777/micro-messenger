FROM python:3.9


WORKDIR /code


COPY requirements.txt .


RUN pip install -r requirements.txt

EXPOSE 8080


COPY ../.. .


CMD [ "python3", "./app.py" ]