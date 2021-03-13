import logging

from newsie import config
from newsie.newsapi_helper import NewsApiHelper
from newsie.slack import SlackFacade


def main(news_api_helper):

    sf = SlackFacade()

    for query in config.QUERIES:
        # get results
        result = news_api_helper.get_top_headlines(query)
        logging.info(f"Retrieved {result['totalResults']} results.")
        articles = result["articles"]

        # send to slack
        sf.send_messages(
            query.name,
            articles,
            query.slack_channel
        )


if __name__ == "__main__":
    main(NewsApiHelper())