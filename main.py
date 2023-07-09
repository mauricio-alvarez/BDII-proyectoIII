import face_recognition
import random,os,math,cv2,time, rtree, pickle, heapq,json,time, heapq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rtree.index import Index

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

def saveDict(diccionario, archivo):
    with open(archivo, 'w') as file:
        json.dump(diccionario, file)

def saveCharacteristics(filename):
    path = "C:/Users/Administrador/Desktop/UTEC/BASE DE DATOS 2/lfw"
    folders = os.listdir(path)
    metadataJSON = dict()
    contador = 0
    with open(filename, 'wb') as f:
        for i, folder in enumerate(folders):
            files = os.listdir(path+"/"+folder)
            for j, file in enumerate(files):
                image = face_recognition.load_image_file(path+"/"+folder+"/"+file)
                print(path+"/"+folder+"/"+file)
                
                try:
                    np.array(face_recognition.face_encodings(image)[0]).tofile(f)
                    metadataJSON[contador] = path+"/"+folder+"/"+file
                    contador+=1
                except :
                    print("Error")

    saveDict(metadataJSON,filename+'_metadata.txt')


def parComparison(comparaciones, vectores):
    resultados = list()
    for i in range(comparaciones):
        num1 = random.randint(0, 13175)
        num2 = random.randint(0, 13175)
        resultados.append(np.linalg.norm(vectores[num1] - vectores[num2]))
    return resultados

def knnSequential(lista_valores, query, k):
    heap = []
    
    for valor in lista_valores:
        distancia = np.linalg.norm(valor - query)
        heapq.heappush(heap, (distancia, valor))
        
        # Si la cola de prioridad supera el tamaño K, eliminamos el elemento más lejano
        if len(heap) > k:
            heapq.heappop(heap)
    return heap

def rangeSearch(lista_valores, query, r):
    result = list()
    for valor in lista_valores:
        distanciaE = np.linalg.norm(valor - query)
        if(distanciaE <= r):
            result.append(distanciaE,valor)

    return result

def buildRindex(vectors):
    
    #1- borrando archivos anteriores
    if os.path.exists("128-index.data"):
        os.remove("128-index.data")
    if os.path.exists("128-index.index"):
        os.remove("128-index.index") 
    

    # 2- configurar el indice
    prop = rtree.index.Property()
    prop.dimension = 128
    prop.buffering_capacity = 3 # M
    prop.dat_extension = "data"
    prop.idx_extension = "index"

    ind = rtree.index.Index('128-index', properties = prop)

    # 3- insertar los puntos
    for i in range(len(vectors)):
        ind.insert(i, vectors[i])

def loadRIndex(filename):
    prop = rtree.index.Property()
    prop.dimension = 128
    prop.buffering_capacity = 3 # M
    prop.dat_extension = "data"
    prop.idx_extension = "index"
    ind = rtree.index.Index("128-index", properties=prop)
    return ind




#saveCharacteristics("faceEncodings.bin")

vectores = loadNVectors("faceEncodings.bin",50)

#k_vecinos = knnSequential(vectores,vectores[50],2)
#print(k_vecinos)

buildRindex(vectores)
loadRIndex()



