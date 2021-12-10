import string #Métodos para limpiar cadenas
import pandas as pd #Para trabajar como DataFrame -> Algoritmo TF-IDF
import numpy as np #Para realizar cálculos
import re 
import json #Crear archivos JSON
import requests #"re" -> consulta las páginas web 
from bs4 import BeautifulSoup #
from sklearn.feature_extraction.text import TfidfVectorizer      
#https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html


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

    #print(q)
    print("\n")
    q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
    #print(q_vec)

    sim = {}

    # Cálculo de la similitud
    for i in range(len(df.columns)):
        sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
        #print(sim[i])

    # Ordenamiento de los vaores
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
    # Print the articles and their similarity values
    print("*************************************")
    print("   resultados para: ",q)
    print("*************************************\n")
    for k, v in sim_sorted:
        if v != 0.0:
            print(documents[k]["titulo"])
            print("Valor de similitud:", v, "\n")
            resultados.append(documents[k])
    return resultados



def obtener_imagen():
    site= 'https://www.gaceta.unam.mx/'
    r = requests.get(site);
    soup = BeautifulSoup(r.content, 'html.parser')
    link = [] #Se almacenan todos los links (notas) dispoibles en la página root (site) 
    for i in soup.find('div', {'class':'wpb_column bs-vc-column vc_column_container vc_col-sm-8 vc_hidden-xs vc_custom_1601597157137 vc_col-has-fill'}).find_all('a'): #Encuentra la etiqueta "<a>" del contenedor de la nota
        i['href'] = i['href'] + '?page=all' #Ecuentra el atributo "href"
        link.append(i['href']) #Se agrega el link a lista
    link=pd.unique(link) #Elimine elementos repetidos. 

    noticia={"titulo":"","resumen":"", "fecha":"", "autor":"","nota":"", "gaceta":"", "img":"","ref":""} #El modelo de la Ficha Técnica de las Notas.
    documents = [] #Almacena todas la fichas técnicas
    exp_gaceta=re.compile('https://www.gaceta.unam.mx/tag/g[0-9]+') #Expresión regular par aobtener el número de gaceta
    for i in link:
        autor=fecha=titulo=gaceta=img=ref="" ####

        r = requests.get(i) #Hacemos consulta a la página
    
        soup = BeautifulSoup(r.content, 'html.parser') #Manejamos la consulta como un HTML
    
        sen = [] #Contenido de la nota
        try:
            img= soup.find('img',{'class':'size-full'})["data-src"]#Obtenemos la primera imagen de la nota, cuyo atributo HTML sea "data-src"
        except:
            try:
                img= soup.find('img',{'class':'size-full'})["src"]##Obtenemos la primera imagen de la nota, cuyo atributo HTML sea "src"
            except:
                img= "Sin imagen previa" #La nota no cuenta con imagen previa
        try:
            ref= i; #Almacenamos el link de la página actual
            titulo=soup.find('span',{'class':'post-title'}).text #Almacenamos el título de la nota
            fecha= soup.find('time',{'class':'post-published updated'}).text #Almacenamos la fecha de la nota
            autor= soup.find('span',{'class':'autor'}).text #Almacenamos el autor d ela nota
            gaceta= soup.find('a',{'rel':'tag', 'href': exp_gaceta}).text #Almacenamos el número de gaceta
        
            try:
                resumen= soup.find('h2',{'class':'post-subtitle'}).text #Almacenamos el resumen de la nota
            except:
                resumen= "Sin resumen disponible" #No contiene resumen la nota
            for a in soup.find('div',{'class':'single-container'}).find_all('p'):#Obtenemos la nota en una sola cadena
                sen.append(a.text)

            #Llenando ficha técnica de la nota
            if(len(sen)!=0): 
                noticia["nota"]=''.join(sen)
                noticia["titulo"]=titulo
                noticia["resumen"]=resumen
                noticia["fecha"]=fecha
                noticia["autor"]=re.sub(r'[^\x00-\x7F]+', ' ', normalize(autor))
                noticia["gaceta"]=re.sub(r'[^\x00-\x7F]+', ' ', normalize(gaceta))
                noticia["img"]= img
                noticia["ref"]=ref
                documents.append(noticia.copy())
        except:
            print("No es noticia ", i)
        
    with open ('data.json', 'w') as file:
        json.dump(documents, file, indent=2)
    

def motor(query, documents):
    df_corpus = pd.DataFrame(documents, columns=['autor','fecha','gaceta','nota','ref','resumen','titulo','img'])
    df_corpus['nota'] = df_corpus['nota'].map(lambda x: x.lstrip('+-').rstrip('aAbBcC'))
    vectorizer = TfidfVectorizer()      # Creación de la instancia de TfidfVectorizer en el objeto vectorizer
    X = vectorizer.fit_transform(df_corpus['nota'])
    X = X.T.toarray()
    # Create a DataFrame and set the vocabulary as the index
    df = pd.DataFrame(X, index=vectorizer.get_feature_names())
    resultados= get_similar_articles(normalize(query), df, vectorizer, documents)
    return json.dumps(resultados)            
