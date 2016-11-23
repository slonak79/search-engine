import json
from collections import Counter as counter

TWEETFILE = open("../tweetFile.txt", "r")


class TweetRank:
    """
    TF: Term Frequency, which measures how frequently a term occurs in a document.
    Since every document is different in length, it is possible that a term would
    appear much more times in long documents than shorter ones. Thus, the term
    frequency is often divided by the document length (aka. the total number of
    terms in the document) as a way of normalization:

    TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).

    IDF: Inverse Document Frequency, which measures how important a term is.
    While computing TF, all terms are considered equally important. However
    it is known that certain terms, such as "is", "of", and "that", may appear
    a lot of times but have little importance. Thus we need to weigh down the
    frequent terms while scale up the rare ones, by computing the following:

    IDF(t) = log_e(Total number of documents / Number of documents with term t in it).

    TF-IDF = TF*IDF
    """
    tweetDictionay = {}
    invertedIndex = {}
    hashtags = []
    tweetsById = {}
    breaker = 0

    # gather 1000 tweets
    # NOTE search for a way to use all tweets.
    for tweet, n in enumerate(TWEETFILE):
        if n == 10000:
            break
        tweetDictionay[n] = tweet

    for singleTweet in tweetDictionay:
        try:
            tweet = json.loads(tweetDictionay[singleTweet])
            if "entities" in tweet:
                for tags in tweet['entities']['hashtags']:
                    if tags and 'text' in tags:
                        try:
                            # collect all hashtags
                            hashtags.append(tags['text'])

                        except AttributeError:
                            print('\n\n' + 'Attribute Error')
                            print(tags)
                # aggregate tags
                hashtagCount = counter(hashtags)
                # dict of tweets where key = tweet id, value: tweet
                # TODO - don't have to store entire tweet, we can store only the tweet id and retrive the entire tweet throuh the Twitter API
                tweetsById[tweet["id"]] = tweet

                for k, v in hashtagCount.items():
                    if k in invertedIndex:
                        invertedIndex[k][0] += v
                        # store individual count of tag per document
                        invertedIndex[k][1].append([tweet["id"], v])
                    else:
                        invertedIndex[k] = [v, [[tweet["id"], v]]]

        except TypeError:
            print("Type Error occurred")
            print(singleTweet)
            continue

    # turn indivivual count into rank
    for k, v in invertedIndex.items():
        for doc in v[1]:
            doc[1] = float(doc[1]) / float(v[0])

    def searchByTagText(self, tag):
        """
        :rtype: object
        """
        try:
            # NOTE come up with a clever way to use the ranking
            # OBSERVATION: some tweets have more than one tag
            return {tag: TweetRank.tweetsById[TweetRank.invertedIndex[tag][1][0][0]]["text"]}
        except:
            return "not found"

    def searchByTagTweet(self, tag):
        """
        :rtype: object
        """
        try:
            return {tag: TweetRank.tweetsById[TweetRank.invertedIndex[tag][1][0][0]]}

        except:
            return "not found"
