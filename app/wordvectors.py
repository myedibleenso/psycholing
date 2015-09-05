import pymongo
from pymongo import MongoClient
import numpy as np

class WordVector(object):
    def __init__(self, word, vector, neighbors=dict()):
        self.word = word
        self.vector = np.asarray(vector)
        self.neighbors = neighbors
        self.db_entry = {"_id": self.word,
                         "word": self.word,
                         "vector": self.vector.tolist(),
                         "neighbors":self.neighbors}

    def cosine_similarity(self, other, N=8):
        sim = np.dot(self.vector, other.vector) / (np.linalg.norm(self.vector) * np.linalg.norm(other.vector))
        return float('{score:.{dec}f}'.format(score=sim, dec=N))

class ScoredPair(object):
    def __init__(self, w1, w2, score):
        self.w1 = w1
        self.w2 = w2
        self.score = score

class Score(object):
    def __init__(self, w, score):
        self.word = w
        self.score = score
        self.pair = (self.score, self.word)


# def most_similiar(wv1):
#     max_pair = None
#     for v in collection.find():
#         wv2 = wordvector_from_db(v)
#         if wv1.word != wv2.word:
#             sim_score = cosine_similarity(wv1, wv2)


class WordVectorCollection(object):

    def __init__(self, wv_collection):
        self.collection = wv_collection

    def query_collection(self, query):
        return self.collection.find(query)

    def retrieve_wordvector(self, word):
        wv = self.collection.find_one({"word": word})
        return WordVector(wv["word"], wv["vector"], wv.get("neighbors", dict())) if wv else None

    def wordvector_from_db(self, dbobj):
        return WordVector(dbobj['word'], dbobj['vector'], dbobj['neighbors'])

client = MongoClient()
db = client.wordvectors
w2v_collection = WordVectorCollection(db.w2v)
