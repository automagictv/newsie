# Requirements

 * Must accept queries or categories for areas I'm interested in.
 * Must accept sources if I want to limit to specific publications.
 * Should integrate with the News API to retrieve top headlines for each category/query.
 * Should integrate with Slack where we will receive the suggested articles.
 * Should provide functionality to post separate categories to separate channels.
 * Each Slack post should include the article, publication, description and a link to the article.

# Design

 * News Helper Interface
    * Connects to a news API
    * Queries top headlines based on config
 * Slack API Interface
    * Connects to the API
    * Structures data in desired message format
    * Sends messages to a specified channel
 * Query object
    * Encapsulate all query logic and performs data checks if needed
    * Map a query to a channel
    * Map a query to the name of our result set
 * Config
    * House all constants / settings
    * Contain an iterable of query objects
 * Runner
    * Use the objects to implement the behavior we want and execute the program

# Happy Path

 1. Use config file to get a set of queries we want to use for our article search.
 2. Iterate over categories / queries and call a news api for each to get top results.
 3. Format Slack messages according to preferred style/layout.
 4. Send Slack messages to the specified channel.
 5. Exit.

# Expansion Ideas

 * If the publication allows scraping, you can render the article in slack.
 * If the publication allows scraping, summarize the article using NLP.
 * Add integration with Pocket to save articles for later.
 * Add sharing functionality to share articles straight from Slack.
