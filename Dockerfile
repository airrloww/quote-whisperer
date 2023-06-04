FROM python:3.9.16

WORKDIR /app

ADD . /app

RUN pip install requirements.txt

# CMD ["python3", "whisperer_app.py"]