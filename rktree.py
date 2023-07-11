import pickle

from scipy.spatial import KDTree

class Kdtree:
    def __init__(self):
        self.filename = 'kdtree.pickle'

    def GoSecondMemory(self, vectors):
        tree = KDTree(vectors, 2)
        with open(self.filename, 'wb') as file:
            pickle.dump(tree, file)

    def recoveryVector(self):
        with open(self.filename, 'rb') as file:
            kdtree = pickle.load(file)
        return kdtree

    def searchknn(self, vector, k):
        tree = self.recoveryVector()
        dist, ind = tree.query(vector, k=k)
        # dist distancia de la query a sus cercanos
        # ind los vectores que estan cerca
        return ind  # esto de aca debemos hashear para recuperar las fotos
