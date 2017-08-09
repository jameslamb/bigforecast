import newspaper
from newspaper import Article


from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def article_to_dict(a):
    a_dict = {}
    a_dict['title'] = a.title
    a_dict['text'] = a.text
    a_dict["keywords"] = a.keywords
    a_dict["source"] = a.source_url
    a_dict["num_images"] = len(a.images)
    a_dict["date"] = a.publish_date
    a_dict["url"] = a.url
    return a_dict

def load_article(a, es, i):
    es.index(index = "news",
             doc_type="article",
             id = i,
             body = article_to_dict(a))

def load_source_url(url, starting_id):
    paper = newspaper.build(url, memoize_articles = False)
    i = starting_id
    fails = 0
    for article in paper.articles:
        try:
            article.download()
            article.parse()
            article.nlp()
            print(article.title, i)
            load_article(article, es, i)
            i += 1
        except:
            fails += 1
            continue
    print("Fails:", fails)
    print("Out of:", paper.size())

def count_total_query():
    #es.search(index = "news",
              #doc_type = "article",
              #body = "query")
    return es.count(index = "news",
             doc_type = "article")


if __name__ == "__main__":
    load_cnn = False
    load_fox = False
    load_msnbc = False

    if load_cnn is True:
        c = count_total_query()
        load_source_url("http://cnn.com", starting_id = c['count'] + 1)

    if load_fox is True:
        c = count_total_query()
        load_source_url("http://fox.com", starting_id = c['count'] + 1)

    if load_msnbc is True:
        c = count_total_query()
        load_source_url("http://msnbc.com", starting_id = c['count'] + 1)

        c = count_total_query()
        print(c['count'], "Articles now in the index.")

    else:
        c = count_total_query()
        print(c['count'], "Articles already in the index.")


    get_first = False
    if get_first is True:
        for i in [1,2,3,4,5]:
            print(es.get(index = "news", doc_type = "article", id = i))

