import os
from math import ceil

from flask import Flask, render_template, abort, \
    make_response, redirect, send_from_directory

import articles

app = Flask(__name__)

DIR = './articles'
PER_PAGE = 5
articles = articles.Articles(DIR)
DEBUG = False


@app.route('/')
def index():
    a = articles.get_articles()
    display = a[:PER_PAGE]
    more = True if a > display else False
    response = make_response(
        render_template(
            'index.html',
            articles=display,
            more=more,
            debug=DEBUG
        )
    )
    response.headers['Cache-Control'] = 'max-age=3600'
    return response


@app.route('/articles/')
@app.route('/articles/<int:page_num>')
def articles_list(page_num=1):
    page_num = int(page_num)
    if page_num == 1:
        return redirect('/', 301)
    a = articles.get_articles()
    display = a[(page_num-1)*PER_PAGE:page_num*PER_PAGE]
    if not display:
        abort(404)
    response = make_response(
        render_template(
            'index.html',
            articles=display,
            current_page=page_num,
            pages=range(1, int(ceil(len(a)/float(PER_PAGE)))+1),
            debug=DEBUG
        )
    )
    response.headers['Cache-Control'] = 'max-age=3600'
    return response


@app.route('/article/<url_code>')
def article(url_code=None):
    article = articles.get_article(url_code)
    if not article:
        abort(404)
    return render_template(
        'article.html',
        article=article,
        debug=DEBUG
    )


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/robots.txt')
def robots():
    return """User-agent: *
Disallow: 
"""


@app.route('/articles/view/<url_code>')
def legacy_article(url_code):
    return redirect('/article/{0}'.format(url_code), 301)


@app.route('/categories/')
@app.route('/categories/view/<url_code>')
def legacy_categories(*args, **kwargs):
    abort(410)


def get_extra_files(extra_dirs):
    if not type(extra_dirs) is list:
        extra_dirs = [extra_dirs]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)
    return extra_files

if __name__ == '__main__':
    import sys
    DEBUG = True
    extra_files = get_extra_files(["./templates/", "./articles/"])
    app.run('0.0.0.0', debug=DEBUG, extra_files=extra_files)
