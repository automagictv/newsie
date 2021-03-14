import os

from newsie.query_helper import QueryHelper


LOGFILE = os.environ.get("LOGFILE", "/tmp/newsielog")

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_BOT_NAME = os.environ.get("SLACK_BOT_NAME", "Newsie")
DEFAULT_SLACK_CHANNEL = os.environ.get("DEFAULT_SLACK_CHANNEL", "#newsie")

# Pytz timezone string. You can see a full list here:
# https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
# or by calling pytz.all_timezones
TIMEZONE = "America/New_York"

# Valid 2 letter The 2-letter ISO 3166-1 code (lowercase).
# E.g. "us" for USA. Defaults to all.
COUNTRY_CODE = "us"

# Query objects for us to use in our application
QUERIES = [

    QueryHelper(
        name="Crypto News",
        query="cryptocurrency"
    ),

    QueryHelper(
        name="Science News",
        category="science",
        country=COUNTRY_CODE
    ),

    QueryHelper(
        name="Tech News",
        sources=[
            "ars-technica",
            "wired",
        ]
    )

]