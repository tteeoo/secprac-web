# docker build -t website .
# docker run -dit -p 1010:1010 --name website website
FROM alpine:3.7

RUN apk update && \
    apk add py3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY . /app

CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:1010", "wsgi"]
