import os
import sys
sys.path.insert(0, os.path.realpath(os.path.dirname(__file__) + '/../'))

import unittest

import articles
import time


class TestArticle(unittest.TestCase):

    def test_instancenorulcode(self):
        metadata = {
            'title': 'Hello World',
            'date': '2012-10-21',
            'tags': ['js']
        }
        content = '#Hello World'
        article = articles.Article(metadata, content)
        self.assertEquals(article.title, metadata['title'])

        self.assertTrue(type(article.date) is time.struct_time)
        self.assertEquals(article.date.tm_year, 2012)
        self.assertEquals(article.date.tm_mon, 10)
        self.assertEquals(article.date.tm_mday, 21)

        self.assertEquals(article.tags, ['js'])

    def test_articlestr(self):
        metadata = {
            'title': 'Hello World',
            'date': '2012-10-21',
            'tags': ['js']
        }
        content = '#Hello World'
        article = articles.Article(metadata, content)
        expected = '''date: '2012-10-21'
tags: [js]
title: Hello World

#Hello World'''
        self.assertEquals(expected, str(article))


class TestArticles(unittest.TestCase):

    ENTRIES = {'file1.md': '''title: Testing
url_code: testing
date: 2012-07-25
tags:
    - js
    - node

This is an entry
================

 - First thing
 - Second thing''',
               'file2.md': '''title: Testing 2
url_code: testing-2
date: 2012-05-25
tags:
    - scala
    - data-mining

Processing Streams
==================

 - First thing
 - Second thing'''}

    DIR = os.path.realpath(os.path.dirname(__file__) + '/fixtures/')

    def setUp(self):
        try:
            os.rmdir(self.DIR)
        except:
            pass
        try:
            os.mkdir(self.DIR)
        except:
            pass
        for filename in self.ENTRIES:
            with open(self.DIR + '/' + filename, 'w+') as f:
                f.write(self.ENTRIES[filename])

    def tearDown(self):
        for filename in self.ENTRIES:
            try:
                os.unlink(self.DIR + '/' + filename)
            except:
                pass
        try:
            os.rmdir(self.DIR)
        except:
            pass


class TestGetArticles(TestArticles):

    def test_getarticlefromfile(self):
        article = articles.get_article_from_file(self.DIR + '/file1.md')
        self.assertEquals('Testing', article.title)
        self.assertEquals(['js', 'node'], article.tags)

    def test_getarticlesfromdir(self):
        articles_in_dir = articles.get_articles_from_dir(self.DIR)
        url_code = 'testing'
        self.assertEquals(url_code, articles_in_dir[url_code].url_code)


class TestArticlesForApp(TestArticles):

    def test_getorderedarticles(self):
        a = articles.Articles(self.DIR)
        by_date = a.get_articles()
        for article in by_date[1:]:
            previous = by_date[by_date.index(article) - 1]
            self.assertTrue(previous.date >= article.date)

    def test_getarticebyurlcode(self):
        a = articles.Articles(self.DIR)
        article = a.get_article('testing')
        self.assertTrue(type(article) is articles.Article)
        self.assertEquals(article.title, 'Testing')

if __name__ == '__main__':
    unittest.main()
