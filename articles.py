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
        print("In _get_articles")
        if not self.articles:
            print("Instance variable articles didn't exist")
            self.articles = get_articles_from_dir(self.directory)
            print("Got articles")
        return self.articles

    def get_articles(self):
        print("In get_articles")
        if not self.articles_by_date:
            print("Instance variable articles_by_date didn't exist")
            unordered = self._get_articles()
            print("Got unordered articles")
            articles_list = [
                unordered[url_code] for url_code in unordered
            ]
            print("Got articles into list")
            self.articles_by_date = sorted(
                articles_list, key=lambda a: a.date, reverse=True)
            print("Sorted articles by date")
        return self.articles_by_date

    def get_article(self, url_code):
        articles = self._get_articles()
        return articles.get(url_code)


def get_article_from_file(filename):
    newline = '\n'
    with open(filename) as f:
        data = f.read()
    # Replace any carriage returns
    data = data.replace('\r', '')
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
    print("Getting articles from {0}".format(directory))
    if directory[-1] != '/':
        directory += '/'
    print("Directory is now {0}".format(directory))
    articles_list = glob('%s*.%s' % (directory, EXT))
    print("Got the glob")
    articles = {}
    for file in articles_list:
        print("Processing file {0}".format(file))
        article = get_article_from_file(file)
        print("Got article")
        articles[article.url_code] = article
        print("Url code is {0}".format(article.url_code))
    return articles
