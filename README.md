# slack

This is the slack integration for [InfraBox](https://infrabox.net). You can simply add this to your build definition by adding a git job like this:

```json
{
    "type": "git",
    "name": "external",
    "clone_url": "https://github.com/InfraBox/slack.git",
    "commit": "master"
}
```

To configure the Slack Webhook URL you have to create a secret with the name **SLACK_WEBHOOK_URL** and the url as value.

Tip: It's best to run the slack job as last job, because it will only report the status of all the parent jobs.

See also the [slack examples](https://github.com/InfraBox/examples/tree/master/slack).

That's it, you should now receive slack message for each build executed on InfraBox.
