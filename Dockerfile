# docker build -t secprac --build-arg name="Ubuntu 18 practice" .
# docker run -dit -p 1008:1008 --name secprac secprac
FROM alpine:latest

ARG name="Practice image"
ARG timezone="America/New_York"

RUN apk update && \
    apk add py3-pip python3-dev tzdata
RUN ln -sf /usr/share/zoneinfo/"$timezone" /etc/localtime

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY . /app
RUN rm -rf web/json/
RUN python3 configure.py "$name"

CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:1008", "wsgi"]
