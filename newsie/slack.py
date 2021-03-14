import logging
import datetime

import dateutil.parser
import pytz
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from newsie import config


SLACK_BOT_TEXT = (
    "Hey there! I found a few articles you may be interested in. "
    "I've listed them below. If you want to read the full article, "
    "click on the button.\n\n*I hope you read something interesting!*\n"
)


class SlackFacade(object):

    def __init__(self, token=config.SLACK_BOT_TOKEN,
                 bot_name=config.SLACK_BOT_NAME):
        self.token = token
        self.default_channel = config.DEFAULT_SLACK_CHANNEL
        self.bot_name = bot_name

        # Internally set properites
        self.client = self._get_slack_client()
        self.icon_emoji = ":newspaper:"
        self.slack_message_entries = {}

    def _get_slack_client(self):
        """Gets a slack client authorized using the provided token.
        
        Returns a `SlackClient` object.
        """
        return WebClient(token=self.token)

    def emit(self, blocks, channel):
        """Sends a message to your channel.

        Args:
            blocks: Expected to be a json-like array object containing the rich
                text representation of the listings we've found. The methods in
                this object should be used to construct the Rich Message Blocks.
                See the Slack kit builder for more information on block
                construction: https://app.slack.com/block-kit-builder
            channel: string, The channel to send the message to.
        """
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text="Newsie Incoming!",
                blocks=blocks,
                # as_user must be false to set bot name
                username=self.bot_name,
                icon_emoji=self.icon_emoji
            )
        except SlackApiError as e:
            logging.error(f"Slack encountered an error: {e.response['error']}")
            raise e

        return response

    def send_messages(self, name, articles, channel=None, n=8):
        """Sends messages after chunking data to comply with slack limits.

        Should chunk data, create rich message layouts, and send the message.

        Args:
            name: string, name of this search.
            articles: An iterable of newsapi article responses.
            channel: string, the channel for these messages.
            n: The size of our final chunks. This is needed to break up
                our messages to avoid slacks block limits (50):
                https://api.slack.com/reference/block-kit/blocks
        """
        channel = channel or self.default_channel
        # Prep data and get final keys
        final_articles = self._chunk_message_data(articles, n=n)
        message_count = len(final_articles)

        logging.info(f"Sending listings via Slack in {message_count} messages.")

        # Send message block sets
        for ind, articles in enumerate(final_articles):
            if ind == 0:
                message = self.create_rich_message_layout(name, articles, cont=False)
            else:
                message = self.create_rich_message_layout(name, articles, cont=True)
            slack_response = self.emit(message, channel)
            logging.info(f"Sent message {ind+1}/{message_count} to Slack:\n{slack_response}")


    def _chunk_message_data(self, articles, n=8):
        """Prepares the data objects for use by x.

        Args:
            session: An initialized SQLAlchemy session.
            articles: An iterable of newsapi article responses.
            n: The size of our final chunks. This is needed to break up
                our messages to avoid slacks block limits (50):
                https://api.slack.com/reference/block-kit/blocks
        Returns:
            A list of chunked articles.
        """
        logging.info("Preparing slack message data...")
        # Chunk data
        logging.info("Chunking data...")
        final_message_keys = [
            articles[i:i + n] for i in range(0, len(articles), n)
        ]

        return final_message_keys

    def format_divider_block(self):
        """Returns a divider block."""
        return {"type": "divider"}

    def format_button_block(self, url):
        """Formats a button block that takes the user to the article.

        See the documentation for more on block elements:
            https://api.slack.com/reference/block-kit/block-element

        Args:
            url: String of the url for the article.
        Returns:
            A properly formatted button block.
        """
        return {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Read the Full Article",
                    },
                    "value": "article_link",
                    "url": url
                }
            ]
        }

    def format_article_block(self, headline, description, source, publish_dt, image_url):
        """Formats an article block for the slack payload.

        Desired layout:

            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Title*: source | publish_dt\ndescription."
                },
                "accessory": {
                    "type": "image",
                    "image_url": "image_url",
                    "alt_text": "alt text for image"
                }
            }

        Args:
            headline: string, the headline for the article.
            description: string, the description of the article.
            publish_dt: datetime, the utc date the article was published.
            source: string, the name of the source for the article.
            image_url: string, url for the article's image.
        Returns:
            A properly formatted article block (see above) as a dict.
        """
        tzone = pytz.timezone(config.TIMEZONE)
        tz_dt = publish_dt.replace(tzinfo=pytz.utc).astimezone(tzone)
        dt_string = tzone.normalize(tz_dt).strftime("%Y-%m-%d %H:%M:%S")
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{headline.capitalize()}*\n{source} | {dt_string}\n{description}."
            },
            "accessory": {
                "type": "image",
                "image_url": f"{image_url}",
                "alt_text": "alt text for image"
            }
        }

    def parse_dt(self, dtstring):
        """Parses the dt string and returns datetime obj.
        
        Args:
            dtstring: string, represeting the published date.
        Returns:
            datetime.datetime in utc.
        """
        try:
            datetime_obj = datetime.datetime.strptime(dtstring, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            datetime_obj = dateutil.parser.parse(dtstring)
        return datetime_obj.replace(tzinfo=pytz.utc)

    def format_article_blocks(self, articles):
        """Formats a rich message layout block for the specified article set.

        Args:
            articles: A list of newsapi respponse articles results.
        Returns:
            Dict representing the proper rich message block layout.
        """
        blocks = [self.format_divider_block()]

        for article in articles:
            headline = article["title"]
            description = article["description"]
            url = article["url"]
            image_url = article["urlToImage"]
            source = article["source"]["name"]
            publish_dt = self.parse_dt(article["publishedAt"])

            article_block = self.format_article_block(
                headline, description, source, publish_dt, image_url)
            button_block = self.format_button_block(url)
            blocks.append(article_block)
            blocks.append(button_block)

        return blocks

    def format_header_block(self, name, cont=False):
        """Method to return a static block header.

        This will be the full Slack message header whenever it posts.

        Args:
            name: string, the name of the search.
            cont: bool, indicating if this is a continued message or not.
        Returns:
            List of the first block depending on if we're continuing or not.
        """
        first_block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": SLACK_BOT_TEXT if not cont else "Articles continued..."
            }
        }
        if not cont:
            header = {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{name.capitalize()}"
                }
            }
            return [header, first_block]
        else:
            return [first_block]

    def create_rich_message_layout(self, name, articles, cont=False):
        """Returns a properly formatted array representation of ordered blocks.

        See Slack's documentation for more info on Rich Message Layouts:
        https://api.slack.com/messaging/composing/layouts

        For our application, it's expected that the blocks will look like this:

            [
                # Header block
                # Article 1
                # Article 2
                # ...
            ]

        See the block element reference for more context on blocks:
        https://api.slack.com/reference/block-kit/block-elements

        Args:
            articles: A list of dicts representing article results from newsapi.
            cont: Bool indicating if this is a continuation of a massage.
        Returns:
            A properly formatted array representing a Slack Rich Message Layout.
        """
        blocks = self.format_header_block(name, cont)
        blocks.extend(self.format_article_blocks(articles))
        return blocks
