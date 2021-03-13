import pytest

from newsie import query_helper


class TestQueryHelper:

    def test_query_helper_raises_for_sources_and_cat_and_country(self):
        """Tests that we raise if sources and country or sources and cat are set."""
        with pytest.raises(ValueError, match=query_helper.ERROR_TEXT):
            query_helper.QueryHelper(
                "test", "test", category="test", country="test", sources=["test"]
            )

    def test_query_helper_raises_for_sources_and_country(self):
        """Tests that we raise if sources and country or sources and cat are set."""
        with pytest.raises(ValueError, match=query_helper.ERROR_TEXT):
            query_helper.QueryHelper(
                "test", "test", country="test", sources=["test"]
            )

    def test_query_helper_raises_for_sources_and_cat(self):
        """Tests that we raise if sources and country or sources and cat are set."""
        with pytest.raises(ValueError, match=query_helper.ERROR_TEXT):
            query_helper.QueryHelper(
                "test", "test", category="test", sources=["test"]
            )

    def test_params_match_expected_no_sources(self):
        """Tests that query parameters match constructor args."""
        inputs = {
            "name": "test",
            "query": "querytest",
            "category": "category",
            "country": "us",
            "language": "en",
            "slack_channel": "#channel",
        }

        obj = query_helper.QueryHelper(**inputs)

        for param in inputs.keys():
            assert obj.__dict__[param] == inputs[param]

    def test_params_match_expected_with_sources(self):
        """Tests that query parameters match constructor args."""
        inputs = {
            "name": "test",
            "query": "querytest",
            "language": "en",
            "slack_channel": "#channel",
            "sources": ["test", "test"]
        }

        obj = query_helper.QueryHelper(**inputs)

        for param in inputs.keys():
            assert obj.__dict__[param] == inputs[param]
