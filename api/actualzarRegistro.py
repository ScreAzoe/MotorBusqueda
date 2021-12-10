
from os import error
import pandas as pd #Para trabajar como DataFrame -> Algoritmo TF-IDF
import re 
import json #Crear archivos JSON
import requests #"re" -> consulta las páginas web 
from bs4 import BeautifulSoup #
   

def cabecera():
    print("\n")
    print("-------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------")
    print("\\\\                                                                     //")
    print("//       xxxxxxxx xxxxx xxx    xxx  xxxxxxx  xxxxxxxx xxxxxxx          \\\\")
    print("\\\\       xxxxxxxx xxxxx xxxx   xxx  xxxxxxxx xxxxxxxx xxxxxxxx         //")
    print("//       xxx       xxx  xxxxx  xxx  xx    xx xxx      xxx   xxx        \\\\")
    print("\\\\       xxxxxx    xxx  xxxxxxxxxx  xx    xx xxxxxxx  xxxxxxxx         //")
    print("//       xxxxxx    xxx  xxxxxxxxxx  xx    xx xxxxxxx  xxxxxxx          \\\\")
    print("\\\\       xxx      xxxxx xxx   xxxx  xxxxxxxx xxx      xxx   xxx        //")
    print("//       xxx      xxxxx xxx    xxx  xxxxxxx  xxxxxxxx xxx    xxx       \\\\")
    print("\\\\                                                                     //")
    print("-------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------")

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

def agregarLista(datos):
    lista=[]
    try:
        with open('articulos.json') as file:
            lista=json.load(file)
            lista.extend(datos)
            return lista
    except:
        return datos
    

def eliminarDuplicado(datos):
    data =[dict(t) for t in {tuple(d.items()) for d in datos}]
    return data


def agregarDocumento(data):
        with open ('articulos.json', 'w') as file:
            json.dump(data, file, indent=2)
        return len(data)

def obtenerImagen():
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
            try:
                gaceta= soup.find('a',{'rel':'tag', 'href': exp_gaceta}).text #Almacenamos el número de gaceta
            except:
                gaceta="No Disponible"
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
                noticia["gaceta"]=gaceta
                noticia["img"]= img
                noticia["ref"]=ref
                documents.append(noticia.copy())
        except:
            pass
    return agregarDocumento(eliminarDuplicado(agregarLista(documents)))

if __name__ == '__main__':
    cabecera()
    try: 
        numeroNotas= obtenerImagen()
        print("\n\n-------------------------------------------------------------------------")
        print("                       >> Actulización Terminada <<                      ")
        print("-------------------------------------------------------------------------")
        print("\nRegistro Actual: ", numeroNotas, " artículos")
    except:
        print("\n\n-------------------------------------------------------------------------")
        print("                            >>    Error    <<                            ")
        print("-------------------------------------------------------------------------")
        print("\nVerifica tu conexión a internet o dispoinibilidad del sitio: ")
        print("             https://www.gaceta.unam.mx/")




