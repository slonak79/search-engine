import json
from collections import Counter as counter
# TODO no need for this global variable, place it in __ini__ method


class TweetRank:
    """
    TF: Term Frequency, which measures how frequently a term occurs in a document.
    Since every document is different in length, it is possible that a term would
    appear much more times in long documents than shorter ones. Thus, the term
    frequency is often divided by the document length (aka. the total number of
    terms in the document) as a way of normalization:
#
    TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).

    IDF: Inverse Document Frequency, which measures how important a term is.
    While computing TF, all terms are considered equally important. However
    it is known that certain terms, such as "is", "of", and "that", may appear
    a lot of times but have little importance. Thus we need to weigh down the
    frequent terms while scale up the rare ones, by computing the following:

    IDF(t) = log_e(Total number of documents / Number of documents with term t in it).

    TF-IDF = TF*IDF
    """
    # TODO create a method, generateTF(), that calculates the Term Frequency
    # TODO create a method, generateIDF(), that calculates the Inverse Document Frequency
    def __init__(self):
        self.selftweetDictionay = {}
        self.invertedIndex = {}
        self.hashtags = []
        self.tweetsById = {}
        self.tweetFilePath = "../tweetFile.txt"

    # gather 1000 tweets
    # NOTE search for a way to use all tweets.
    # TODO the loop on row 40 is redundant, combine with loop on line 45
    for tweet, n in enumerate(TWEETFILE):
        if n == 10000:
            break
        tweetDictionay[n] = tweet
    # TODO separate code in loop below, its doing too much
    for singleTweet in tweetDictionay:
        try:
            tweet = json.loads(tweetDictionay[singleTweet])
            if "entities" in tweet:
                for tags in tweet['entities']['hashtags']:
                    if tags and 'text' in tags:
                        try:
                            # collect all hashtags from a tweet
                            hashtags.append(tags['text'])

                        except AttributeError:
                            print('\n\n' + 'Attribute Error')
                            print(tags)
                # aggregate tags
                hashtagCount = counter(hashtags)
                #TODO - don't have to store entire tweet, we can store only the tweet id and retrive the entire tweet throuh the Twitter API
                # dict of tweets where key = tweet id, value: tweet
                tweetsById[tweet["id"]] = tweet

                for k, v in hashtagCount.items():
                    if k in invertedIndex:
                        invertedIndex[k][0] += v
                        # TODO too much data duplication, fix it
                        # store individual count of tag per document
                        invertedIndex[k][1].append([tweet["id"], v])
                    else:
                        invertedIndex[k] = [v, [[tweet["id"], v]]]

        except TypeError:
            print("Type Error occurred")
            print(singleTweet)
            continue

    # TODO fix how rank is been calculated.
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
