import pandas as pd #Para trabajar como DataFrame -> Algoritmo TF-IDF
import numpy as np #Para realizar cálculos
import json #Crear archivos JSON
from sklearn.feature_extraction.text import TfidfVectorizer      
#https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html


orden=""



#CAMBIA EL NOMBRE DEL MES POR NÚMERO PARA POSTERIORMENTE HACER EL ORDENAMIENTO

def ordenarFecha(documents):
#CAMBIA EL NOMBRE DEL MES POR NÚMERO PARA POSTERIORMENTE HACER EL ORDENAMIENTO
    fechascam = (
            ("Ene", "01"),
            ("Feb", "02"),
            ("Mar", "03"),
            ("Abr", "04"),
            ("May", "05"),
            ("Jun", "06"),
            ("Jul", "07"),
            ("Ago", "08"),
            ("Sep", "09"),
            ("Oct", "10"),
            ("Nov", "11"),
            ("Dic","12")
        ) #Para cambiar los meses por su correspondiente número
    for dicc in documents:
        for a, b in fechascam:
            dicc["fecha"] = dicc["fecha"].replace(a, b).replace(a.upper(), b.upper()) #Remplaza Mes por número

    for diccionario in documents:
        diccionario["fecha"] = diccionario["fecha"].replace(",", "")#Quita coma en el día
        diccionario["fecha"] = diccionario["fecha"].replace(" ", "/")#Agrega / para separa la fecha

    arreglafecha = (
            ("/1/", "/01/"),
            ("/2/", "/02/"),
            ("/3/", "/03/"),
            ("/4/", "/04/"),
            ("/5/", "/05/"),
            ("/6/", "/06/"),
            ("/7/", "/07/"),
            ("/8/", "/08/"),
            ("/9/", "/09/")
    ) #Para agregar un "0" en las fechas de 1 dígito
    for diccionario in documents:
        if len(diccionario["fecha"]) == 9:
            for a, b in arreglafecha:
                diccionario["fecha"] = diccionario["fecha"].replace(a, b).replace(a.upper(), b.upper()) 
    #ORDENA DICCIONARIO POR FECHA
    documents=sorted(documents, key = lambda i: i["fecha"])
    return documents

def ordenarAutor(documents):
    #AGREGA "DESCONOCIDO" A LAS FICHAS QUE NO TIENEN AUTOR
    for diccionario in documents:
        if len(diccionario["autor"]) <= 3:
            diccionario["autor"]= "Desconocido"
    #ORDENA DICCIONARIO POR Autor
    documents=sorted(documents, key = lambda i: i["autor"])
    return documents
    
def ordenarSimilitud(sim, documents):
    # Ordenamiento de los vaores
    resultados=[]
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
    for k, v in sim_sorted:
        if v != 0.0:
            print(documents[k]["titulo"])
            print("Valor de similitud:", v, "\n")
            resultados.append(documents[k])
    return resultados


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ñ","n")
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

#https://towardsdatascience.com/create-a-simple-search-engine-using-python-412587619ff5

def get_similar_articles(q, df, vectorizer, documents):
    resultados=[]
  
    # Convirtiendo la consulta en un vector
    q = [q]

    q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)

    sim = {}

    # Cálculo de la similitud
    for i in range(len(df.columns)):
        sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)

    print("*************************************")
    print("   resultados para: ",q)
    print("*************************************\n")
    resultados= ordenarSimilitud(sim, documents)
    if orden==1:
        resultados= ordenarAutor(resultados)
    elif orden==2:
        resultados= ordenarFecha(resultados)
    return resultados


    

def motor(query, documents, opcion):
    global orden
    orden= float(opcion)
    df_corpus = pd.DataFrame(documents, columns=['autor','fecha','gaceta','nota','ref','resumen','titulo','img'])
    df_corpus['nota'] = df_corpus['nota'].map(lambda x: x.lstrip('+-').rstrip('aAbBcC'))
    vectorizer = TfidfVectorizer()      # Creación de la instancia de TfidfVectorizer en el objeto vectorizer
    X = vectorizer.fit_transform(df_corpus['nota'])
    X = X.T.toarray()
# Creación del dataframe (filas=vocabulario (palabras), columnas = documentos (artículos de Gaceta UNAM))
    df = pd.DataFrame(X, index=vectorizer.get_feature_names())
    resultados= get_similar_articles(normalize(query), df, vectorizer, documents)
    return json.dumps(resultados)            
