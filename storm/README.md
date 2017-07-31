# Apache Storm in Bigforecast

Apache storm is used for streaming our input data into HDFS.  Storm is fed
from a kafka queue.


## Actions storm performs:

 * Determines relevence of item to commodity price under investigation
 * Scrapes information from related articles
 * If relevant, determines sentiment and 
 * Outputs information to modelling system
 * Loads all data into HDFS
 
## Spouts

*  Consumes from kafka

Sources:
    * GDELT 15 minute updates
    * Twitter?



## Bolts

There are two basic paths 

* Scraper Bolt
     * Takes the URL of the story and goes and grabs the whole story
     * Scrapes relevant web content for news item

* Relevance Bolt
    * Determines relevance of news item to time series being tracked (oil price)
    * Plan to train a supervised learning algorithm using a set of oil financial
    news articles and then classify incoming articles against that as relevant
    or not relevant and also return the probability.
    
* Implication Bolt
    * Try to train a supervised learning algorithm on news events in the past and
    the oil price fluctuation of that day, that week, and that month to see what
    types of articles are relevant.
    
* Sentiment / Impact Bolt
    * Determines the potential implication of the article / event on the value.
    * Another type of Implication bolt?
    
* Loader Bolt
    * Writes to appropriate HDFS directory
    
