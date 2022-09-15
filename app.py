from flask import Flask, render_template, jsonify
from main import topHashtagsQuery

app = Flask(__name__)
app.config['MONGODB_URI'] = 'mongodb://localhost:27017/'


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/tophashtags')
def topHashtags():
    res = topHashtagsQuery()
    print(res)
    return res


if __name__ == '__main__':
    app.run()