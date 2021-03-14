import pytest
import datetime

import pytz

from newsie import config
from newsie import slack


class TestSlack:

    client = slack.SlackFacade()

    def test_get_slack_client_gets_client(self, mocker):
        """Tests that a client is retrieved and assigned to the client var."""
        mocker.patch.object(slack, "WebClient", autospec=True)
        fkey = "TEST"
        _ = slack.SlackFacade(fkey)
        slack.WebClient.assert_called_once_with(fkey)

    def test_emit_message_calls_post_message(self, mocker):
        """Tests that our emit message method calls post message endpoint."""
        mocker.patch.object(slack, "WebClient", autospec=True)
        helper = slack.SlackFacade()
        blocks = ['blocks']
        channel = '#fk'
        _ = helper.emit(blocks, channel)
        helper.client.chat_postMessage.assert_called_once_with(
            channel=channel,
            text="Newsie Incoming!",
            blocks=blocks,
            username=helper.bot_name,
            icon_emoji=helper.icon_emoji
        )

    def test_chunk_message_data_chunks_data_for_n(self):
        """Tests that we're correctly chunking data."""
        articles = [fake for fake in range(16)]
        expected = [[n for n in range(8)], [n for n in range(8, 16)]]
        tested = self.client._chunk_message_data(articles, 8)
        assert tested == expected

    def test_format_divider_block_formats(self):
        """Tests that the divider is properly formatted."""
        assert self.client.format_divider_block() == {"type":"divider"}

    def test_format_button_block_formats(self):
        """Tests that the button block is properly formatted."""
        url = "www.fake.com"
        expected = {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Read the Full Article",
                    },
                    "value": "article_link",
                    "url": f"{url}" 
                }
            ]
        }
        assert self.client.format_button_block(url) == expected

    def test_format_article_block_returns_expected(self):
        """Tests that an article block is returned as expected."""
        utc_dt = datetime.datetime(2021, 3, 1, 1, 1, 1).replace(
            tzinfo=pytz.utc)

        tzone = pytz.timezone(config.TIMEZONE)
        tz_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(tzone)
        expected_dt = tzone.normalize(tz_dt).strftime("%Y-%m-%d %H:%M:%S")
        expected = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Title*\nsource | {expected_dt}\ndescription."
            },
            "accessory": {
                "type": "image",
                "image_url": "image_url",
                "alt_text": "alt text for image"
            }
        }

        assert self.client.format_article_block(
            "title", "description", "source", utc_dt, "image_url"
        ) == expected

    def test_parse_dt_returns_with_expected_format(self):
        """Tests that the expected date format works."""
        dtstring = "2021-01-01T12:12:14Z"
        expected = datetime.datetime(2021, 1, 1, 12, 12, 14, tzinfo=pytz.utc)
        assert self.client.parse_dt(dtstring) == expected

    def test_parse_dt_returns_with_unexpected_format(self):
        """Tests that an unexpected date format works."""
        dtstring = "2021-01-01 12:12:14"
        expected = datetime.datetime(2021, 1, 1, 12, 12, 14, tzinfo=pytz.utc)
        assert self.client.parse_dt(dtstring) == expected

    def test_format_article_blocks_returns_expected(self):
        """Tests that formatting the article blocks returns expected."""
        utc_dt = datetime.datetime(2021, 3, 1, 1, 1, 1).replace(
            tzinfo=pytz.utc)

        tzone = pytz.timezone(config.TIMEZONE)
        tz_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(tzone)
        expected_dt = tzone.normalize(tz_dt).strftime("%Y-%m-%d %H:%M:%S")
        expected = [
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Title*\nsource | {expected_dt}\ndescription."
                },
                "accessory": {
                    "type": "image",
                    "image_url": "www.image.com",
                    "alt_text": "alt text for image"
                }
            }, {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Read the Full Article",
                        },
                        "value": "article_link",
                        "url": "www.com"
                    }
                ]
            }

        ]

        input_obj = [{
            "title": "Title",
            "description": "description",
            "url": "www.com",
            "urlToImage": "www.image.com",
            "source": {"name": "source"},
            "publishedAt": "2021-03-01T01:01:01Z"
        }]

        assert self.client.format_article_blocks(input_obj) == expected

    def test_format_header_block_returns_header(self):
        """Tests that the header returns as expected."""
        name = "tester"
        expected = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{name.capitalize()}"
                }
            }, {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{slack.SLACK_BOT_TEXT}"
                }
            }
        ]

        assert self.client.format_header_block(name) == expected

    def test_format_header_block_returns_continued(self):
        """Tests that the header block returns continued."""
        name = "tester"
        expected = [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Articles continued..."
            }
        }]

        assert self.client.format_header_block(name, cont=True) == expected

    def test_create_rich_message_layout_returns_expected(self):
        """Tests that the rich message returns as expected."""
        utc_dt = datetime.datetime(2021, 3, 1, 1, 1, 1).replace(
            tzinfo=pytz.utc)

        tzone = pytz.timezone(config.TIMEZONE)
        tz_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(tzone)
        expected_dt = tzone.normalize(tz_dt).strftime("%Y-%m-%d %H:%M:%S")
        name = "tester"
        input_obj = [{
            "title": "Title",
            "description": "description",
            "url": "www.com",
            "urlToImage": "www.image.com",
            "source": {"name": "source"},
            "publishedAt": "2021-03-01T01:01:01Z"
        }]

        expected = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{name.capitalize()}"
                }
            }, {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{slack.SLACK_BOT_TEXT}"
                }
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Title*\nsource | {expected_dt}\ndescription."
                },
                "accessory": {
                    "type": "image",
                    "image_url": "www.image.com",
                    "alt_text": "alt text for image"
                }
            }, {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Read the Full Article",
                        },
                        "value": "article_link",
                        "url": "www.com"
                    }
                ]
            }
        ]

        assert self.client.create_rich_message_layout(name, input_obj) == expected

    def test_create_rich_message_layout_returns_expected_continued(self):
        """Tests that the rich message returns as expected."""
        utc_dt = datetime.datetime(2021, 3, 1, 1, 1, 1).replace(
            tzinfo=pytz.utc)

        tzone = pytz.timezone(config.TIMEZONE)
        tz_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(tzone)
        expected_dt = tzone.normalize(tz_dt).strftime("%Y-%m-%d %H:%M:%S")
        name = "tester"
        input_obj = [{
            "title": "Title",
            "description": "description",
            "url": "www.com",
            "urlToImage": "www.image.com",
            "source": {"name": "source"},
            "publishedAt": "2021-03-01T01:01:01Z"
        }]

        expected = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Articles continued..."
                }
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Title*\nsource | {expected_dt}\ndescription."
                },
                "accessory": {
                    "type": "image",
                    "image_url": "www.image.com",
                    "alt_text": "alt text for image"
                }
            }, {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Read the Full Article",
                        },
                        "value": "article_link",
                        "url": "www.com"
                    }
                ]
            }
        ]

        assert self.client.create_rich_message_layout(name, input_obj, cont=True) == expected
