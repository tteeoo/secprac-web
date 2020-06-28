# docker build -t secprac .
# docker run -dit -p 1008:1008 --name secprac secprac
FROM alpine:3.7

RUN apk update && \
    apk add py3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY . /app

CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:1008", "wsgi"]
