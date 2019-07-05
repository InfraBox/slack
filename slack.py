import os
import sys
import json

import requests


def main():
    job = json.load(open("/infrabox/job.json", "r"))

    if job.get("local", False):
        print("Local job, not sending message")
        return

    print(json.dumps(job, indent=4))
    if "SLACK_WEBHOOK_URL" not in os.environ:
        print("SLACK_WEBHOOK_URL not set")
        sys.exit(1)

    slack_webhook_url = os.environ["SLACK_WEBHOOK_URL"]

    jobs = job.get("parent_jobs", [])
    attachments = []

    success = True
    for j in jobs:
        state = j["state"]
        if state in ("finished", "running", "skipped"):
            # do nothing
            pass
        elif state == "failure":
            success = False
            attachments.append({"color": "#cc5965", "text": f"{j['name']}: Job failed"})
        else:
            success = False
            attachments.append(
                {"color": "#000000", "text": f"{j['name']}: Job unknown state: {state}"}
            )

    build_url = job["build"]["url"]
    name = job["project"]["name"]
    branch = job["commit"]["branch"]
    # Optional, from environment
    cron_job_name = os.getenv("INFRABOX_CRONJOB_NAME")
    tag_name = os.getenv("INFRABOX_GIT_TAG")

    if success:
        message = ":white_check_mark: Successfully finished build"
    else:
        message = ":x: Build failed"

    text = f"{message} for *{name}* on branch: *{branch}*"
    if cron_job_name:
        text += f" triggered by cron: *{cron_job_name}*"
    if tag_name:
        text += f" for tag: *{tag_name}*"
    text += f"\n{build_url}"

    data = {
        "text": text,
        "username": "InfraBox",
        "icon_emoji": ":infrabox:",
        "attachments": attachments,
    }

    print("sending message")
    r = requests.post(slack_webhook_url, json=data)

    print(r.text)


if __name__ == "__main__":
    main()
