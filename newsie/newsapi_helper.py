import logging

from newsapi import NewsApiClient

from newsie import config


class NewsApiHelper(object):

    def __init__(self, api_key=config.NEWS_API_KEY):
        """Constructor for our API interface."""
        self.client = NewsApiClient(api_key=api_key)

    def get_top_headlines(self, query):
        """Returns the top headlines.

        Args:
            query: An instantiated query_helper.QueryHelper object.
        Returns:
            Top headlines.
        """
        logging.info(f"Retrieveing top headlines for {query}...")
        articles = self.client.get_top_headlines(
            q=query.query,
            language=query.language,
            country=query.country,
            category=query.category,
            sources=",".join(query.sources) if query.sources else None,
            page_size=100
        )
        logging.info(f"Retrieved {len(articles['articles'])} articles")
        return articles
