import pymongo
from pymongo import MongoClient
import numpy as np
import heapq

class WordVector(object):
    """
    A storage class that to encapsulate a db entry as a word and its corresponding vector & KNNs
    """
    def __init__(self, word, vector, neighbors=dict()):
        self.word = word
        self.vector = np.asarray(vector)
        self.neighbors = neighbors

    def db_entry(self):
        """
        A shortcut for producing the db entry from a WordVector instance (useful for updates).
        """
        return {"_id": self.word,
                "word": self.word,
                "vector": self.vector.tolist(),
                "neighbors": self.neighbors}

    def cosine_similarity(self, other, N=8):
        """
        Compute the cosine similarity of two WordVector instances
        """
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


class WordVectorCollection(object):
    # the number of nearest neighbors to find
    K = 10
    def __init__(self, wv_collection):
        self.collection = wv_collection
        self.timeout = 200

    def query_collection(self, query):
        """
        Search the db using the provided query.
        """
        return self.collection.find(query)

    def retrieve_wordvector(self, word):
        """
        Attempt to retrieve a db entry for a case-folded word.
        Search is limited by a set timeout.
        """
        try:
            # attempt a lowercase query
            wv = self.collection.find_one({"word": word.lower()}, max_time_ms=self.timeout)
        except:
            print("query for '{0}' exceeded {1} ms timeout...".format(word, self.timeout))
            wv = None
        return WordVector(wv["word"], wv["vector"], wv.get("neighbors", dict())) if wv else None

    def wordvector_from_db(self, dbobj):
        """
        Create a WordVector instance from a database entry.
        """
        return WordVector(dbobj['word'], dbobj['vector'], dbobj['neighbors'])

    def compare_all(self, word):
        """
        Find the nearest K neighbors by cosine similarity in the db for the provided word.
        """

        def retrieve_neighbors(wv):
            """
            Find the nearest K neighbors by cosine similarity in the db for the provided entry.
            Returns a generator.
            """
            for entry in self.collection.find():
                other_wv = self.wordvector_from_db(entry)
                # Do not compare the same words
                if other_wv.word != wv.word:
                    yield (wv.cosine_similarity(other_wv), other_wv)

        def sort_neighbors(neighbors):
            """
            Sort the dict of (WordVector, score) pairs as a descending seq.
            of (score, word) pairs.
            """
            return sorted(neighbors.items(), key= lambda x: x[-1], reverse=True)

        wv = self.retrieve_wordvector(word)
        # Did we find an entry for the provided word?
        if not wv:
            return None
        # If we don't already have K neighbors stored...
        if len(wv.neighbors) != WordVectorCollection.K:
            # Get the KNN
            nearest_neighbors = heapq.nlargest(WordVectorCollection.K, retrieve_neighbors(wv))
            # create a dict of (score, word) pairs from the KNNs
            neighbors = {wv.word:score for (score, wv) in nearest_neighbors}
            # update the WordVector's neighbors
            wv.neighbors = neighbors
            # attempt to update the db entry with the computed KNN
            try:
                self.collection.save(wv.db_entry())
            except Exception as e:
                print("Couldn't update entry...")
                print(e)

        return sort_neighbors(wv.neighbors)


############ interact with the w2v db ##############
client = MongoClient()
db = client.wordvectors
w2v_collection = WordVectorCollection(db.w2v)

# MP solution (TODO)
#import multiprocessing as mp
#nproc = multiprocessing.cpu_count()
#pool = mp.Pool(processes=nproc)
#pool.map(cosine_similarity, xrange(1000))
# def compare_terms(w1, w2, N=8):
#     """
#     Compute the cosine similarity of two WordVector instances
#     """
#     sim = np.dot(w1.vector, w2.vector) / (np.linalg.norm(w1.vector) * np.linalg.norm(w2.vector))
#     return float('{score:.{dec}f}'.format(score=sim, dec=N))
