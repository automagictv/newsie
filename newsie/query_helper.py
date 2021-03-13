
ERROR_TEXT = "Sources can not be set if country or category is set."


class QueryHelper(object):

    def __init__(self, name, query=None, category=None, country=None, 
                 sources=None, language=None, slack_channel=None):
        """Constructs the query helper object.

        Args:
            name: string, The name for this query (used in Slack).
            query: string, The query to use. Advanced search is available:
                Surround phrases with quotes (") for exact match.
                Prepend words or phrases that must appear with a + symbol. Eg: +bitcoin
                Prepend words that must not appear with a - symbol. Eg: -bitcoin
                Alternatively you can use the AND / OR / NOT keywords,
                    and optionally group these with parenthesis.
                    Eg: crypto AND (ethereum OR litecoin) NOT bitcoin.
            category: string, One of business, entertainment, general, health, science
                sports, technology. Cannot be set if sources is set.
            country: string, The 2-letter ISO 3166-1 code (lowercase) for the country.
                Cannot be set if sources is set.
            sources: list, String sources valid for the api. Obtainable from
                https://newsapi.org/sources or by calling the sources endpoint.
                Cannot be set if category or country is set.
            language: string, The 2-letter ISO-639-1 code of the language
                you want to get headlines for. Defaults to "en".
            slack_channel: string, the #channel name where these results will be
                published.
        Raises:
            ValueError if sources is set with country or category.
        """
        if sources is not None and (country is not None or category is not None):
            raise ValueError(ERROR_TEXT)

        self.name = name
        self.query = query
        self.category = category
        self.country = country
        self.sources = sources
        self.language = language
        self.slack_channel = slack_channel
