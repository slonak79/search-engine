from collections import Counter as counter
from flask import Flask, request, jsonify, make_response, current_app
import json
twt = open("../tweetFile.txt","r")

from datetime import timedelta
from functools import update_wrapper
from flask.ext.cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/search/', methods=['POST'])
def hello():
    print "HELLO"
    tags=request.form['tags']

    result = searchByTagText(tags)
    print result
    tagged = {"tags": result}
    return jsonify(tagged)


twtDict = {}
invertedIndex = {}
hashtags = []
tweetsById = {}
breaker = 0

i = 0


for t in twt:
    if (breaker == 10000):
        break
    twtDict[i] = t
    i += 1
    breaker += 1

for tw in twtDict:

    try:
        t = json.loads(twtDict[tw])
        if "entities" in t:
            for tags in t['entities']['hashtags']:
                if tags and 'text' in tags:
                    try:
                        hashtags.append(tags['text'])

                    except AttributeError:
                        print '\n\n' + 'Attribute Error'
                        print tags

            hashtag_dict = counter(hashtags)
            #dict of tweets where key = tweet id, value: tweet
            tweetsById[t["id"]] = t

            for k, v in hashtag_dict.iteritems():
                if k in invertedIndex:
                    invertedIndex[k][0] += v
                    #store individual count of tag per document
                    invertedIndex[k][1].append([t["id"], v])
                else:
                    invertedIndex[k] = [v, [[t["id"], v]]]

    except TypeError:
        print "Type Error occurred"
        print tw
        continue

#turn indivivual count into rank
for k, v in invertedIndex.iteritems():
    for doc in v[1]:
        doc[1] = float(doc[1])/float(v[0])



def searchByTagText(tag):
    """
    :rtype: object
    """
    try:
        #TODO come up with a clever way to use the ranking
        #OBSERVATION: some tweets have more than one tag
        return {tag:tweetsById[invertedIndex[tag][1][0][0]]["text"]}
    except:
        return "not found"


def searchByTagTweet(tag):
    """
    :rtype: object
    """
    try:
        return {tag:tweetsById[invertedIndex[tag][1][0][0]]}

    except:
        return "not found"


# print 'Inverted Index'
# for key in invertedIndex:
#     print key




if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int("3000")
    )
