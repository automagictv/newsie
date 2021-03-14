# Requirements

 * Must accept queries or categories for areas I'm interested in.
 * Must accept sources if I want to limit to specific publications.
 * Should integrate with the News API to retrieve top headlines for each category/query.
 * Should integrate with Slack where we will receive the suggested articles.
 * Should provide functionality to post separate categories to separate channels.
 * Each Slack post should include the article, publication, description and a link to the article.

# Happy Path

 1. Call some config file to get a set of queries we want to use for our article search.
 2. Iterate over categories / queries and call the news api for each to get top results.
 3. Format Slack messages according to our preferred Rich Message Layout.
 4. Send Slack messages to the specified channel.
 5. Exit.

# Design

 * News API Interface
 * Slack API Interface
 * Query object
 * Config
 * Runner

# Expansion Ideas

 * If the publication allows scraping, you can render the article in slack.
 * If the publication allows scraping, summarize the article using NLP.
 * Add integration with Pocket to save articles for later.
 * Add sharing functionality to share articles straight from Slack.
