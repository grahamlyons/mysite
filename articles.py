import yaml
import markdown2
from glob import glob
import re
from time import strptime, strftime
import datetime

EXT = 'md'
DATEFORMAT = '%Y-%m-%d'

class Article(object):

    def __init__(self, metadata, content):
        self.title = metadata.get('title')
        self.url_code = metadata.get('url_code')
        rawdate = metadata.get('date')
        if type(rawdate) is not datetime.date:
            self.date = strptime(rawdate, DATEFORMAT)
        else:
            self.date = rawdate
        self.tags = metadata.get('tags')
        self.rawcontent = content

    @property
    def content(self):
        return markdown2.markdown(self.rawcontent)

    def __str__(self):
        metadata = {
            'title': self.title,
            'date': strftime(DATEFORMAT, self.date),
            'tags': self.tags
        }
        if self.url_code:
            metadata['url_code'] = self.url_code
        return '%s\n%s' % (yaml.dump(metadata), self.rawcontent)

class Articles(object):

    def __init__(self, directory):
        self.articles = None
        self.articles_by_date = None
        self.directory = directory

    def _get_articles(self):
        if not self.articles:
            self.articles = get_articles_from_dir(self.directory)
        return self.articles

    def get_articles(self):
        if not self.articles_by_date:
            unordered = self._get_articles()
            articles_list = [unordered[url_code] for url_code in unordered] 
            self.articles_by_date = sorted(articles_list, key=lambda a: a.date, reverse=True)
        return self.articles_by_date

    def get_article(self, url_code):
        articles = self._get_articles()
        return articles.get(url_code)

def get_article_from_file(filename):
    newline = '\n'
    with open(filename) as f:
        data = f.read()
    lines = data.split(newline)
    endofmeta = lines.index('')
    metadata = yaml.load(newline.join(lines[:endofmeta]))
    content = newline.join(lines[endofmeta+1:])
    return Article(metadata, content)

def generate_url_code(title, articles):
    length = 50
    code = title.replace(' ', '-').lower()
    code = re.sub('[^a-z0-9-]', '', code)
    code = code[:length]
    i = 2
    replacement = code
    while code in articles:
        code = replacement + str(i)
        replacement = code[:len(code)-1] 
        i += 1
    return code

def get_articles_from_dir(directory):
    if directory[-1] != '/':
        directory += '/'
    articles_list = glob('%s*.%s' % (directory, EXT))
    articles = {}
    for file in articles_list:
        article = get_article_from_file(file)
        articles[article.url_code] = article
    return articles
