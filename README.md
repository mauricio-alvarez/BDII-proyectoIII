# BDII-proyecto3
## ***Integrantes:***
- Mauricio Alvarez
- Aaron Santamaria
- Rodo Vilcarromero
- Ronaldo Flores
- 
## ***Introducción:***
Para el presente proyecto usamos las librerías face_recognition, numpy, pandas, matplotlib.pyplot, rtree.index importando la libreria Index y scipy.spatial importando la libreria KDTree.


## ***Libreria:***
La base de datos usada en este proyecto consiste de registros de publicaciones académicas por parte de la universidad de Cornell, donde encontramos campos como autores, títulos de artículos, categorías, abstracts y id's para poder ubicarlos en la página de la universidad.

## **GUI** (Frontend)

## ***Dominio de datos:*** (Backend)
- ****
Presenta el código para poder levantar la base de datos con las tablas “articles” , “versions” y “authors_parsed”.
- ****
Contiene un diccionario que asocia el id de documento con la posición en el archivo
- ****
Contiene un diccionario que asocia cada keyword con su id y cuantas veces se repite en el documento
- **Source.py**
Contiene la clase Sequential, con la siguiente estructura:
    - Su objetivo es traer todos los registros de la memoria secundaria
    - init: recibe todos los vectores con los que trabajaremos.
    - knnSequential: usa una cola de prioridad, luego itera con los vectores, para calcular la distancia euclidiana con la función np.linalg.norm() teniendo como único parametro la diferencia entre la query y el vector, si la cola de prioridad supera el tamaño K, eliminamos el elemento más lejano.
    - rangeSearch: le pasamos el Radio como parametro, iteramos todos los vectores, calculamos la misma distancia euclidiana y si menor a radio lo agregamos a una lista para luego retornarlo.

Contiene la clase RtreeIndex, con la siguiente estructura:
    - buildRindex: Le pasamos los vectores que queremos almacenar en un archivo r para memoria secundaria
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

- **.py**
Contiene la clase Postgre:
    - connectToDB: conecta la base de datos.
    - loadData: Procesamos los articulos uno a la vez para rellenar cada registro en las tablas de la base de datos. 
    - createIndex:
Esta funcion recibe una lista con los elementos de los articulos que queremos indexar. Ya que solo estamos indexando el titulo y el abstract, solo recibe esos paramentros. En postgresql se asigna relevancia con las letras A,B,C,D entonces para los 4 primeros elementos de la lista se asigna una letra.
Posteriorme se crea un columna tsvector y se llena con los datos del title y abstract, vease que se puso con mas importante al titulo.
    - process_text:
La funcion to_tsquery de postgresql recibe como parametro una consulta preprocesada donde cada keyword se debe separar por un operador booleano, entonces se identifica algunos terminos del ingles asociados a algunos operadores y se los reemplaza en la query consultQuery: Forzamos la busqueda con el indice de los top-k resultados los cuales almacenamos en una lista que se mostrara en la GUI.
	
- **.py**
    - recovery_query: Desglozamos la query para agregarlo a una lista, creamos los stopwords(lista) en query y agregamos  el 'no', 'don´t', 'doesn´t', 'didn´t', 'dont', filtramos por si la  query no es valida, si no es una negacion( lo que agregamos al stopword) lo va a agregar como un true, caso contrario lo agregará como false el query que le sigue al exceptions.

    - serach_document:
Un for en la query desempaquetada, si el valor es verdadero en la palabra, obtendremos todos los documentos de aquella y lo agregamos a Yes_documents, caso contrario lo añadimos en No_documents. y retornamos una diferencia de conjuntos entre Yes_document y No_document.

    - sort_document: 
Itera sobre la lista de indices, abrimos el archivo y luego movemos el puntero en la posicion de bits correspondiente, despues añadimos a documents, posteriormente convertimos el json en un diccionario, para finalizar en titles agregamos el titulo.
Creamos una variable a un vector luego sacamos el tfidf a los documentos, luego sacamos el tfidf de la query, termiando sacando la similitud de coseno entre ellos.
Un ultimo for para el topk con el coseno de similitud con título
    - recoveryDara:Llamamos a todo.
- **Archivos generados por el desarrollo del backend:**
[Descargar archivos](https://drive.google.com/drive/folders/1a20unbmjfS_bZHMhosFUuWpFwGwLTRIz)

