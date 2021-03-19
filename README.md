# newsie

Daily collections of articles straight to Slack (**tutorial video [here](https://youtu.be/tMkuLiCmGzw)**).

## Initial Setup
This uses `pipenv` to manage the virtual env and all dependencies. If you don't have pipenv install it [here](https://pypi.org/project/pipenv/) then:

```
git clone https://github.com/automagictv/newsie.git
cd newsie
pipenv install --ignore-pipfile
```

To run:

```
pipenv run python newsie/runner.py
```

Note that you may have to adjust your python path to run the above. If so, you can run this with:

```
cd newsie
PYTHONPATH=$PYTHONPATH:$(pwd) pipenv run python newsie/runner.py
```

If you want to set this up on a cron, you can do something like:

```
# Run at 12:05 AM every day
5 0 * * * pipenv run python /path/to/newsie/runner.py >> /path/to/cronlog.txt 2>&1
```

You may have to add `/usr/local/bin` to your path for the above to work.

## Config

This uses the `config.py` file to set certain constants, filters and queries when calling slack or news api.

The `QUERIES` object is what is used to retrieve headlines. To add a new query, add an entry to the object using the `newsie/query_helper.py` object, `QueryHelper`.

## Testing

This package uses [pytest](https://docs.pytest.org/en/stable/). So to run the tests, execute the following:

```
pipenv run python -m pytest
```

Or to test an individual module, run:

```
pipenv run python -m pytest tests/[test_module].py
```

## Slack

This uses the [Slack API](https://api.slack.com/) to send news articles to your desired channel. It makes use of the [Rich Message Layout](https://api.slack.com/messaging/composing/layouts) to format the messages. The format we use is as follows:

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

For full instructions on how to set up / connect to the slack api, see [this tutorial](https://github.com/slackapi/python-slack-sdk/blob/main/tutorial/01-creating-the-slack-app.md).
