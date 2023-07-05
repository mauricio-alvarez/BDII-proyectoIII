import face_recognition
import random,os,math,cv2,time, rtree, pickle, heapq,json,time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_encoding(filename, index, encoding_size=128):
    with open(filename, 'rb') as f:
        f.seek(index * encoding_size * 8)
        encoding = np.fromfile(f, dtype=np.float64, count=encoding_size)
    return encoding
def load_all(filename,total):
    data = list()
    for i in range(total):
        data.append(load_encoding(filename, i))
    return data


def save_encodings(encodings, filename):
    with open(filename, 'wb') as f:
        for encoding in encodings:
            np.array(encoding).tofile(f)

def guardar_diccionario(diccionario, archivo):
    with open(archivo, 'w') as file:
        json.dump(diccionario, file)

def guardarCaracterisiticas(filename):
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

    guardar_diccionario(metadataJSON,filename+'_metadata.txt')

#guardarCaracterisiticas("faceEncodings.bin")

def comparacionPares(comparaciones, vectores):
    resultados = list()
    for i in range(comparaciones):
        num1 = random.randint(0, 13175)
        num2 = random.randint(0, 13175)
        resultados.append(np.linalg.norm(vectores[num1] - vectores[num2]))
    return resultados

def knnSequential(k, query):
    pass
def rangeSearch(r, query):
    pass


vectores = load_all("faceEncodings.bin",13176)

#linealScan()
lista = comparacionPares(15000, vectores)
# Crear el histograma
plt.hist(lista, bins=50)
plt.xlabel('Distancia Euclidiana')
plt.ylabel('Frecuencia')
plt.title('Histograma de Distancias Euclidianas 9000')
plt.show()

