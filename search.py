from collections import Counter as counter
from flask import Flask, request, jsonify
import json
twt = open("tweetFile.txt","r")

@app.route('/search/', methods=['POST'])
def hello():
    print "HELLO"
    tags=request.form['tags']
    print tags
    tagged = {"tags": tags}
    return jsonify(tagged)

twtDict = {}
invertedIndex = {}
hashtags = []

breaker = 0

i = 0

for t in twt:
    if (breaker == 10000):
        break
    twtDict[i] = t
    i = i + 1
    breaker += 1

#print json.loads(twtDict[10000])["entities"]["hashtags"][0]["text"]
for tw in twtDict:

    try:
        t = json.loads(twtDict[tw])
        if("entities" in t):
            for tags in t['entities']['hashtags']:
                if tags and 'text' in tags:
                    try:
                        hashtags.append(tags['text'])
                    except AttributeError:  
                        print 'Attribute Error'
                        print tags

            hashtag_dict = counter(hashtags)

            for k, v in hashtag_dict.iteritems():
                if (k in invertedIndex):
                    invertedIndex[k][0] += v
                    invertedIndex[k][1].append(t["id"])
                else:
                    invertedIndex[k] = [v,[t["id"]]]

    except TypeError:
        print "Type Error occurred"
        print tw
        continue

print 'Inverted Index'
for key in invertedIndex:
    print key

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int("3000")
    )
