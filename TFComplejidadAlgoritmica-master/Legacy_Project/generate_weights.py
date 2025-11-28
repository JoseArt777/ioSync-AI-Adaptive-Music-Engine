import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import csv
import ast
import os.path

rango = 4449
df_movies = pd.read_csv('Amdb_5000_movies.csv')

#Overview
headers = ["Source", "Target", "Weight"]
tfidf = TfidfVectorizer(stop_words="english")
df_movies['overview']=df_movies['overview'].fillna("")
tfid_matrix = tfidf.fit_transform(df_movies['overview'])

cosine_sim = linear_kernel(tfid_matrix, tfid_matrix)

indices = pd.Series(df_movies.index, index = df_movies['id']).drop_duplicates()

columna_lista = df_movies['vote_average'].astype(float).tolist()

def generate_overview_recommendations(id, cosine_sim = cosine_sim, cont = 0):
    lis = []
    lista = []
    idx = indices[id]
    sim_scores = cosine_sim[idx]
    for i in sim_scores:
        #i = 10
        i=round(i*100)
        lista = [id,cont,i+columna_lista[cont]]
        if id == cont:
            cont += 1
            continue
        if i <= np.float64(6.0):
            cont +=1
            continue
        #validar que no se hagan relaciones cuando es 0.0
        cont += 1
        lis.append(lista)
    return lis

def get_recommendations_overview():
    file = open("edges_list_overview.csv", "a", newline='')
    writer = csv.writer(file)
    
    writer.writerow(headers)
    for i in range(4449):
        liston = generate_overview_recommendations(i)
        writer.writerows(liston)
    file.close()
        
def overview_is_empty():
    df = pd.read_csv("edges_list_overview.csv")
    return df.empty

def generate_overview():
    if os.path.exists("edges_list_overview.csv") is False:
        get_recommendations_overview()
    elif overview_is_empty():
        get_recommendations_overview()

#Generos
def obtener_ids_por_elemento(input_str):
    ids_por_elemento = []
    data = ast.literal_eval(input_str)
    for elemento in data:
        if 'id' in elemento:
            ids_por_elemento.append(int(elemento['id']))
    return ids_por_elemento

def crear_lista_genero():
    elementos_genero = df_movies['genres'].tolist()

    resultados_genero = []
    for elemento in elementos_genero:
        ids = obtener_ids_por_elemento(elemento)
        resultados_genero.append(ids) 
    return resultados_genero

def generate_genre_recomendations(id, id_genres, cont = 0):
    lis = []
    listita=[]
    for i in id_genres:
        listita=[id,cont,i+columna_lista[cont]]
        if id == cont:
            cont += 1
            continue
        if i <= np.float64(2.0):
            cont +=1
            continue
        cont += 1
        lis.append(listita)
    return lis

def crear_listas_ids_genero(resultados_genero):
    id_genres = []
    for i in range(4449):   
        id_genres.append([sum(valor_genero in otra_lista_genero for valor_genero in resultados_genero[i]) for otra_lista_genero in resultados_genero[0:]])
    return id_genres

def get_recomendations_genre():
    resultados_genero = crear_lista_genero()
    codigos_genero = crear_listas_ids_genero(resultados_genero)
    file2 = open("genres_list.csv", "a", newline='')
    writer2 = csv.writer(file2)

    writer2.writerow(headers)
    for i in range(4449):
        liston2 = generate_genre_recomendations(i, codigos_genero[i])
        writer2.writerows(liston2)
    file2.close()
    
def genre_is_empty():
    df = pd.read_csv("genres_list.csv")
    return df.empty

def generate_genre():
    if os.path.exists("genres_list.csv") is False:
        get_recomendations_genre()
    elif genre_is_empty():
        get_recomendations_genre()

#PC
def obtener_ids_por_elemento_PC(input_str_PC):
    ids_por_elemento_PC = []
    data_PC = ast.literal_eval(input_str_PC)
    for elemento_PC in data_PC:
        if 'id' in elemento_PC:
            ids_por_elemento_PC.append(int(elemento_PC['id']))
    return ids_por_elemento_PC

def crear_lista_PC():
    elementos_PC = df_movies['production_companies'].tolist()

    resultados_PC = []
    for elemento_PC in elementos_PC:
        ids_PC = obtener_ids_por_elemento_PC(elemento_PC)
  
        resultados_PC.append(ids_PC)    

    return  resultados_PC

def generate_PC_recomendations(id, ids_PC, cont = 0):
    lis = []
    listita=[]
    for i in ids_PC:
        listita=[id,cont,i+columna_lista[cont]]
        if id == cont:
            cont += 1
            continue
        if i <= 0:
            cont +=1
            continue
        cont += 1
        lis.append(listita)
    return lis

def crear_listas_ids_PC(resultados_PC):
    id_PC = []
    for i in range(4449):   
        id_PC.append([sum(valor_PC in otra_lista_PC for valor_PC in resultados_PC[i]) for otra_lista_PC in resultados_PC[0:]])
    return id_PC

def get_recomendations_PC():
    resultados_PC = crear_lista_PC()
    codigos_PC = crear_listas_ids_PC(resultados_PC)
    file3 = open("PC_list.csv", "a", newline='')
    writer3 = csv.writer(file3)

    writer3.writerow(headers)

    for i in range(4449):
        liston3 = generate_PC_recomendations(i, codigos_PC[i])
        writer3.writerows(liston3)
    file3.close()

def PC_is_empty():
    df = pd.read_csv("PC_list.csv")
    return df.empty

def generate_PC():
    if os.path.exists("PC_list.csv") is False:
        get_recomendations_PC()
    elif PC_is_empty():
        get_recomendations_PC()

#Generador
def generar_csvs():
    #Overview.csv
    generate_overview()

    #Generos.csv
    generate_genre()
        
    #PC.csv
    generate_PC()