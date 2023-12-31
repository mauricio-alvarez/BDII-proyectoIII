# BDII-proyecto3
## ***Integrantes:***
- Mauricio Alvarez
- Aaron Santamaria
- Rodo Vilcarromero
- Ronaldo Flores
- 
## ***Introducción:***
Para el presente proyecto usamos las librerías face_recognition, numpy, pandas, matplotlib.pyplot, rtree.index importando la libreria Index y scipy.spatial importando la libreria KDTree.
Realizamos  una búsqueda de imagenes basada en similitud utilizando el algoritmo KNN.


## **GUI** (Frontend)

## ***Dominio de datos:*** (Backend)
- **faceEncodings_metadata.json**
Presenta el id y la ruta.
- **faceEncodings.bin**
Estan todos los vectores
- **Source.py**
    - Contiene la clase Sequential, con la siguiente estructura:
        - Su objetivo es traer todos los registros de la memoria secundaria
        - init: recibe todos los vectores con los que trabajaremos.
        - knnSequential: usa una cola de prioridad, luego itera con los vectores, para calcular la distancia euclidiana con la función np.linalg.norm() teniendo como único parametro la diferencia entre la query y el vector, si la cola de prioridad supera el tamaño K, eliminamos el elemento más lejano.
        - rangeSearch: le pasamos el Radio como parametro, iteramos todos los vectores, calculamos la misma distancia euclidiana y si menor a radio lo agregamos a una lista para luego retornarlo.

    - Contiene la clase RtreeIndex, con la siguiente estructura: 
        - buildRindex: Le pasamos los vectores que queremos almacenar en un archivo r para memoria secundaria.
        - Nuestra dimensión es de 128 porque el facereconding nos retorna vectores de 128 x 1
        - Tenemos una capacidad de 3
        - Todo en el archivo "all-index" para la memoria secundaria.
        - loadRIndex: Lo configura y lo lee ademas de q guarda en la variable global ind,desde el archivo en memoria secundaria
        - searchknn: Busca los knn más cercanos y los guarda en searhResults
        - recoverImgs: hace un for en una lista de numeros para luego recuperar las rutas de las imagenes hasheando el id de cada vector y retornamos dicha lista.   

Contiene la clase Kdtree, con la siguiente estructura:
    - Usamos el de la libreria scipy.spatial, siendo el que posee la solucion de escalamiento
    - Guarda las posiciones de los vectores, con ello guardamos la posicion de la lista en la que le pasamos, con una funcion de hash recuperamos la ruta de la imagen para poder mostrarla
    - init: declaramos filename con valor kdtree.pickle.
    - GoSecondMemory:guardar en la memoria secundaria 
    - recoveryVector:recuperar los vectores del rtree
    - searchknn:buscar los **n vectores** más cercanos
    - recoverImgs: Recuperar las imagenes.

- **Experminetos**
![Imagen de WhatsApp 2023-07-12 a las 17 58 50](https://github.com/mauricio-alvarez/BDII-proyectoIII/assets/85258014/8b73d02a-d0de-4d59-8d05-677e182f4f3a)
![Imagen de WhatsApp 2023-07-12 a las 17 55 48](https://github.com/mauricio-alvarez/BDII-proyectoIII/assets/85258014/ff18de7f-5dc7-463f-904b-a4b26d2465ec)
![Imagen de WhatsApp 2023-07-12 a las 17 56 16](https://github.com/mauricio-alvarez/BDII-proyectoIII/assets/85258014/20a13657-4173-4471-bdb1-04f87fc294c2)
![Imagen de WhatsApp 2023-07-12 a las 18 03 23](https://github.com/mauricio-alvarez/BDII-proyectoIII/assets/85258014/46b957ca-f1f4-47a1-a80f-bbb6e299977f)


## **Tiempos**
![image](https://github.com/mauricio-alvarez/BDII-proyectoIII/assets/85258014/a3fcee35-0711-4877-96cd-e3956f07613f)
![image](https://github.com/mauricio-alvarez/BDII-proyectoIII/assets/85258014/e794a06a-bc2a-4ba8-b4c2-7270e700c341)
![image](https://github.com/mauricio-alvarez/BDII-proyectoIII/assets/85258014/986ef9c8-2389-4ea3-a3e8-c64eb075ec9c)

