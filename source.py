import face_recognition
import random,os,math,cv2,time, rtree, pickle, heapq,json,time, heapq, hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rtree.index import Index
from scipy.spatial import KDTree

def loadVector(filename, index, encoding_size=128):
    with open(filename, 'rb') as f:
        f.seek(index * encoding_size * 8)
        encoding = np.fromfile(f, dtype=np.float64, count=encoding_size)
    return encoding

def loadNVectors(filename,total):
    data = list()
    for i in range(total):
        data.append(loadVector(filename, i))
    return data
    
def loadJson(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

class Sequential:
    def __init__(self, lista_valores):
        self.lista_valores = lista_valores
    
    def knnSequential(self, query, k):
        heap = []
        
        for valor in self.lista_valores:
            distancia = np.linalg.norm(valor - query)
            heapq.heappush(heap, (distancia, valor))
            
            # Si la cola de prioridad supera el tamaño K, eliminamos el elemento más lejano
            if len(heap) > k:
                heapq.heappop(heap)
        
        return heap
    
    def rangeSearch(self, query, r):
        result = []
        
        for valor in self.lista_valores:
            distanciaE = np.linalg.norm(valor - query)
            if distanciaE <= r:
                result.append((distanciaE, valor))
        
        return result


class RtreeIndex:
    def __init__(self):
        self.ind = 0
        self.searhResults = 0

    def buildRindex(self, vectors):
        # 1- Borrar archivos anteriores
        if os.path.exists("128-index.data"):
            os.remove("128-index.data")
        if os.path.exists("128-index.index"):
            os.remove("128-index.index") 
    
        # 2- Configurar el índice
        prop = rtree.index.Property()
        prop.dimension = 128
        prop.buffering_capacity = 3  # M
        prop.dat_extension = "data"
        prop.idx_extension = "index"
    
        rindex = rtree.index.Index('all-index', properties=prop)
    
        # 3- Insertar los puntos
        for i in range(len(self.vectors)):
            rindex.insert(i, self.vectors[i])
    
    
    def loadRIndex(self, file):
        prop = rtree.index.Property()
        prop.dimension = 128
        prop.buffering_capacity = 3  # M
        prop.dat_extension = "data"
        prop.idx_extension = "index"
        self.ind = rtree.index.Index(file, properties=prop)


    def searchknn(self, query, k):
        self.searhResults = self.ind.nearest(query, num_results=k)
    
    def recoverImgs(self, files):
        images = list()
        for p in self.searhResults:
            print(files[p])
            images.append(files[p])
        return images


class Kdtree:
    def __init__(self):
        self.filename = 'kdtree.pickle'
        self.ind = 0

    def GoSecondMemory(self, vectors):
        tree = KDTree(vectors, 128)
        with open(self.filename, 'wb') as file:
            pickle.dump(tree, file)

    def recoveryVector(self):
        with open(self.filename, 'rb') as file:
            kdtree = pickle.load(file)
        return kdtree

    def searchknn(self, vector, k):
        tree = self.recoveryVector()
        dist, self.ind = tree.query(vector, k=k)

    def recoverImgs(self, files):
        images = list()
        for i in self.ind:
            print(i, str(i))
            print(files[str(i)])
            images.append(files[str(i)])
        return images
