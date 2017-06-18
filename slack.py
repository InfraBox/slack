import os
import sys
import json

import requests

def main():
    job = json.load(open('/infrabox/job.json', 'r'))

    if job.get('local', False):
        print 'Local job, not sending message'
        return

    if "SLACK_WEBHOOK_URL" not in os.environ:
        print "SLACK_WEBHOOK_URL not set"
        sys.exit(1)

    slack_webhook_url = os.environ["SLACK_WEBHOOK_URL"]

    jobs = job.get('parent_jobs', [])
    attachments = []

    success = True
    for j in jobs:
        if j['state'] == 'finished':
            # do nothing
            pass
        elif j['state'] == 'failure':
            success = False
            attachments.append({
                "color": "#cc5965",
                "text": "%s: Job failed" % j['name']
            })
        elif j['state'] == 'running':
            # do nothing
            pass
        else:
            success = False
            attachments.append({
                "color": "#000000",
                "text": "%s: Job finished" % j['name']
            })

    build_url = job['build']['url']

    if success:
        text = "Successfully finished build"
    else:
        text = "Build failed"

    text += "\n%s" % build_url

    data = {
        "text": text,
        "username": "InfraBox",
        "icon_emoji": ":ghost:",
        "attachments": attachments
    }

    print "sending message"
    r = requests.post(slack_webhook_url, json=data)

    print r.text


if __name__ == "__main__":
    main()
