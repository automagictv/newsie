
from newsie import query_helper
from newsie import newsapi_helper


class TestNewsApiHelper:

    def test_constructor_gets_client(self, mocker):
        """Tests that the constructer gets an api client."""
        mocker.patch.object(
            newsapi_helper, "NewsApiClient", autospec=True
        )
        fkey = "TEST"
        _ = newsapi_helper.NewsApiHelper(fkey)
        newsapi_helper.NewsApiClient.assert_called_once_with(fkey)

    def test_top_headline_getter_calls_client_with_args(self, mocker):
        """Tests that we call the NewsApiClient wtih expected args."""
        mocker.patch.object(
            newsapi_helper, "NewsApiClient", autospec=True
        )
        helper = newsapi_helper.NewsApiHelper("FAKEKEY")
        q = query_helper.QueryHelper(
            name="NAME",
            query="qtest",
            category="cattest",
            country="cotest",
            language="en"
        )
        _ = helper.get_top_headlines(q)

        helper.client.get_top_headlines.assert_called_once_with(
            q=q.query,
            language=q.language,
            country=q.country,
            category=q.category,
            sources=None,
            page_size=100
        )
