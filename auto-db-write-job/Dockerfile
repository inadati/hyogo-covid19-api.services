FROM python:3-alpine

RUN apk --update --no-cache add busybox-static \
    && apk --no-cache add --virtual build-dependencies curl build-base tzdata postgresql-dev gcc python3-dev musl-dev

ENV TZ=Asia/Tokyo
COPY crontab /var/spool/cron/crontabs/root

COPY script /usr/src/script
COPY requirements.txt ./
RUN pip install psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["busybox", "crond", "-f", "-L", "/dev/stderr"]
