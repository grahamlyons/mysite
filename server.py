from math import ceil

from flask import Flask, render_template, abort, make_response, redirect

import articles

app = Flask(__name__)

DIR='./articles'
PER_PAGE=2
articles = articles.Articles(DIR)

@app.route('/', methods=['GET'])
def index():
    a = articles.get_articles()
    display = a[:PER_PAGE]
    more = True if a > display else False
    response = make_response(
        render_template('index.html', articles=display, more=more)
    )
    response.headers['Cache-Control'] = 'max-age=3600'
    return response

@app.route(r'/articles/<page_num>', methods=['GET'])
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
            pages=range(1, int(ceil(len(a)/float(PER_PAGE)))+1)
        )
    )
    response.headers['Cache-Control'] = 'max-age=3600'
    return response

@app.route('/article/<url_code>', methods=['GET'])
def article(url_code=None):
    article = articles.get_article(url_code)
    if not article:
        abort(404)
    return render_template('article.html', article=article)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
