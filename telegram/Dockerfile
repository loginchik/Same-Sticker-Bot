FROM python:3.13-bookworm

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./bot /app/code

CMD ["python", "-m", "code.main"]
