import logging

from newsie import config
from newsie.newsapi_helper import NewsApiHelper
from newsie.slack import SlackFacade


# Set up logging.
logging.basicConfig(
    filename=config.LOGFILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main(news_api_helper, slack_helper):

    for query in config.QUERIES:
        # get results
        result = news_api_helper.get_top_headlines(query)
        logging.info(f"Retrieved {result['totalResults']} results.")
        articles = result["articles"]

        # send to slack
        slack_helper.send_messages(
            query.name,
            articles,
            query.slack_channel
        )


if __name__ == "__main__":
    main(NewsApiHelper(), SlackFacade())