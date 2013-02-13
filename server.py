from math import ceil

from flask import Flask, render_template, abort, make_response, redirect

import articles

app = Flask(__name__)

DIR='./articles'
PER_PAGE=5
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

@app.route('/articles')
@app.route('/articles/')
@app.route('/articles/<page_num>')
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

@app.route('/articles/view/<url_code>')
def legacy_article(url_code):
    return redirect('/article/{0}'.format(url_code), 301)

@app.route('/categories')
def legacy_categories():
    abort(410)

if __name__ == '__main__':
    import sys
    DEBUG = True if '-d' in sys.argv else DEBUG
    app.run('0.0.0.0', debug=DEBUG)
