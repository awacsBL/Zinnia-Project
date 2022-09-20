from flask import Flask, render_template
from main import topHashtagsQuery, topLanguagesQuery, topSourcesQuery

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/top-hashtags')
def topHashtags():
    res = topHashtagsQuery()
    # print(res)
    return res


@app.route('/top-languages')
def topLanguages():
    res = topLanguagesQuery()
    # print(res)
    return res


@app.route('/top-sources')
def topSources():
    res = topSourcesQuery()
    print(res)
    return res

#
# @app.route('/count')
# def countDocuments():
#     res = countAllDocuments()
#     # print(res)
#     return res


if __name__ == '__main__':
    app.run()
