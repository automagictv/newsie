# newsie
Daily collections of articles straight to your Slack.


## Example Slack Rich Message Layout

```
{
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "some text"
    }
},
{
    "type": "divider"
},
{
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "Article"
    },
    "accessory": {
        "type": "image",
        "image_url": "image.jpg",
        "alt_text": "alt text for image"
    }
},
{
    "type": "actions",
    "elements": [
        {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Read the Full Article"
            },
            "value": "article_link",
            "url": "https://www.google.com"
        }
    ]
}
```