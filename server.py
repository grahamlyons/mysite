from flask import Flask, render_template, abort, make_response
import articles
app = Flask(__name__)

DIR='./articles'
articles = articles.Articles(DIR)

@app.route("/")
def index():
    a = articles.get_articles()
    return render_template('index.html', articles=a)

@app.route("/article/<url_code>")
def article(url_code=None):
    article = articles.get_article(url_code)
    if not article:
        abort(404)
    return render_template('article.html', article=article)

if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
