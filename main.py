import os
import re

from bson.son import SON
from bson.json_util import dumps, loads
from dotenv import load_dotenv, find_dotenv
from flask import jsonify
from pymongo import MongoClient

load_dotenv(find_dotenv())

connection_string = os.environ.get("MONGODB_CONNECTION_STRING")
client = MongoClient(connection_string)

db = client["ZinniaProjectDB"]
collection = db["tweets"]


def aggregationQuery(pipeline):
    cursor = collection.aggregate(
        pipeline,
        allowDiskUse=True
    )

    try:
        cursorList = list(cursor)
        jsonData = dumps(cursorList, indent=2)
        return jsonData
    finally:
        cursor.close()


def topHashtagsPipeline(limit: int):
    return [
        {
            u"$unwind": {
                u"path": u"$hashtags",
                u"preserveNullAndEmptyArrays": False
            }
        },
        {
            u"$group": {
                u"_id": u"$hashtags",
                u"tagCount": {
                    u"$sum": 1
                }
            }
        },
        {
            u"$sort": SON([(u"tagCount", -1)])
        },
        {
            u"$limit": limit
        }
    ]


def topLanguagesPipeline(limit: int):
    return [
        {
            '$group': {
                '_id': '$lang',
                'langCount': {
                    '$sum': 1
                }
            }
        },
        {
            '$sort': {
                'langCount': -1
            }
        },
        {
            '$limit': limit
        }
    ]


def topSourcesPipeline():
    return [
        {
            '$group': {
                '_id': '$sourceLabel',
                'sourceCount': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                'sourceCount': -1
            }
        }
    ]


def verifiedUsersPipeline():
    return [
        {
            '$group': {
                '_id': '$user.verified',
                'verifiedCount': {
                    '$sum': 1
                }
            }
        }
    ]


def topTweetsScorePipeline(likeWeight: float, replyWeight: float, retweetWeight: float, quoteWeight: float, limit: int):
    return [
        {
            '$project': {
                '_id': 1,
                'url': 1,
                'date': 1,
                'content': 1,
                'renderedContent': 1,
                'id': 1,
                'user': 1,
                'replyCount': 1,
                'retweetCount': 1,
                'likeCount': 1,
                'quoteCount': 1,
                'lang': 1,
                'media': 1,
                'retweetedTweet': 1,
                'quotedTweet': 1,
                'inReplyToTweetId': 1,
                'inReplyToUser': 1,
                'mentionedUsers': 1,
                'coordinates': 1,
                'place': 1,
                'hashtags': 1,
                'cashtags': 1,
                'likeScore': {
                    '$multiply': [
                        likeWeight, '$likeCount'
                    ]
                },
                'replyScore': {
                    '$multiply': [
                        replyWeight, '$replyCount'
                    ]
                },
                'retweetScore': {
                    '$multiply': [
                        retweetWeight, '$retweetCount'
                    ]
                },
                'quoteScore': {
                    '$multiply': [
                        quoteWeight, '$quoteCount'
                    ]
                }
            }
        }, {
            '$project': {
                '_id': 1,
                'url': 1,
                'date': 1,
                'content': 1,
                'renderedContent': 1,
                'id': 1,
                'user': 1,
                'replyCount': 1,
                'retweetCount': 1,
                'likeCount': 1,
                'quoteCount': 1,
                'lang': 1,
                'media': 1,
                'retweetedTweet': 1,
                'quotedTweet': 1,
                'inReplyToTweetId': 1,
                'inReplyToUser': 1,
                'mentionedUsers': 1,
                'coordinates': 1,
                'place': 1,
                'hashtags': 1,
                'cashtags': 1,
                'likeScore': 1,
                'replyScore': 1,
                'retweetScore': 1,
                'tweetScore': {
                    '$add': [
                        '$likeScore', '$replyScore', '$retweetScore', '$quoteCount'
                    ]
                }
            }
        }, {
            '$sort': {
                'tweetScore': -1
            }
        },
        {
            '$limit': limit
        }
    ]


def topCountriesPipeline():
    return [
        {
            '$project': {
                'country': {
                    '$split': [
                        '$user.location', ' '
                    ]
                },
                'country2': {
                    '$split': [
                        '$user.location', ','
                    ]
                }
            }
        }, {
            '$unwind': {
                'path': '$country'
            }
        }, {
            '$match': {
                'country': re.compile(r"[A-Z]{2}")
            }
        }, {
            '$group': {
                '_id': {
                    'state': '$country'
                },
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                'count': -1
            }
        }
    ]


def topTerms(limit: int):
    return [
        {
            '$project': {
                'terms': {
                    '$split': [
                        '$content', ' '
                    ]
                }
            }
        }, {
            '$unwind': {
                'path': '$terms'
            }
        }, {
            '$group': {
                '_id': '$terms',
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                'count': -1
            }
        }, {
            '$limit': limit
        }
    ]


def topHashtagsQuery():
    return aggregationQuery(topHashtagsPipeline(200))


def topLanguagesQuery():
    return aggregationQuery(topLanguagesPipeline(20))


def topSourcesQuery():
    return aggregationQuery(topSourcesPipeline())


def verifiedUsersQuery():
    return aggregationQuery(verifiedUsersPipeline())


def topTweetsScoreQuery():
    return aggregationQuery(topTweetsScorePipeline(1, 1.5, 2, 2.25, 10))


def countAllDocuments():
    count = collection.count_documents({})
    return jsonify(count)
