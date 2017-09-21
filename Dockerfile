FROM alpine:3.6

RUN apk add --no-cache python py-requests

COPY slack.py /slack.py

CMD python /slack.py
