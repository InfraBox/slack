FROM alpine:3.4

RUN apk add --no-cache python py-requests

COPY slack.py slack.py

CMD python slack.py
