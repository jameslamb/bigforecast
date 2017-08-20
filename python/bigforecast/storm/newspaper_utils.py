import newspaper
from newspaper import Article


def article_to_dict(a):
    a_dict = {}
    a_dict['title'] = a.title
    a_dict['text'] = a.text
    a_dict["keywords"] = a.keywords
    a_dict["source"] = a.source_url
    a_dict["num_images"] = len(a.images)
    a_dict["url"] = a.url
    a_dict["authors"] = a.authors
    return a_dict


def load_article(a, es, i, index="news"):
    es.index(index = index,
             doc_type="article",
             id = i,
             body = a)


def process_article(url):
    a = Article(url, request_timeout = 3)
    a.download()
    a.parse()
    a.nlp()
    return article_to_dict(a)

