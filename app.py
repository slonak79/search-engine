from flask import Flask, request, jsonify, make_response, current_app
import json
from tweetsearch import TweetRank
from datetime import timedelta
from functools import update_wrapper
from flask.ext.cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/search/', methods=['POST'])
def hello():
    print("HELLO")
    tags = request.form['tags']

    result = TweetRank.searchByTagText(tags)
    print(result)
    tagged = {"tags": result}
    return jsonify(tagged)


# print 'Inverted Index'
# for key in invertedIndex:
#     print key


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int("3000")
    )
