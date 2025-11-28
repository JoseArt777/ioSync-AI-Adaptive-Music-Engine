import csv
import os.path
import graphviz as gv

def return_weight(e):
  return e[1]

def compare_weight(e, a):
  if e[1] > a[1]:
    return True
  else:
    False

def addValue(lista, n, qty):
  if len(lista) < qty:
    lista.append(n)
    lista = set(lista)
    lista = list(lista)
  tmp = min(lista, key=return_weight)
  index = lista.index(tmp)
  if compare_weight(n, tmp) and len(lista) >= qty:
    lista.pop(index)
    lista.append(n)
  

def dls(G, n, s, L, qty): 
  print(n)
  visited = [False]*n
  path = [None]*n
  cost = [float('inf')]*n
  lista = []
  
  def _dls(u, L):
     if L > 0 and not visited[u]:
      visited[u] = True
      for v, w in G[u]:
         if not visited[v]:
          cost[v] = w
          path[v] = u
          tupla = (v, w)

          addValue(lista, tupla, qty)
          _dls(v, L - 1)

  _dls(s, L)
  return path, lista


def createGraphFromCSV(csv_file):
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Saltar la primera lÃ­nea (encabezados)
        graph = {}
        for row in reader:
            source = int(row[0])
            target = int(row[1])
            weight = float(row[2])

            if source not in graph:
                graph[source] = []
            if target not in graph:
               graph[target] = []
            graph[source].append((target, weight))
    return graph, source

def return_movies_titles(lista1, lista2):
  lista = []
  for i in lista1:
    lista.append(lista2[i[0]])
  return lista

if os.path.exists("edges_list_overview.csv") is True:    
  G_overview, size1 = createGraphFromCSV("edges_list_overview.csv") #validar esto
  
if os.path.exists("genres_list.csv") is True:    
  G_genre, size2 = createGraphFromCSV("genres_list.csv") #validar esto

if os.path.exists("PC_list.csv") is True:    
  G_studio, size3 = createGraphFromCSV("PC_list.csv") #validar esto

def overview_recomendation(index, qty, peliculas_lista):
    if index != -1:
        path, lista = dls(G_overview, size1, index, 1, qty) #no retornar ni peso ni costo solo dejarlo como comentario para que se vea en la expo
        lista.sort(key=return_weight, reverse=True)
        movies_list = return_movies_titles(lista, peliculas_lista)
        return movies_list, path

def genre_recomendation(index, qty, peliculas_lista):
    if index != -1:
        path, lista = dls(G_genre, size2, index, 1, qty) #no retornar ni peso ni costo solo dejarlo como comentario para que se vea en la expo
        lista.sort(key=return_weight, reverse=True)
        movies_list = return_movies_titles(lista, peliculas_lista)
        return movies_list, path

def PC_recomendation(index, qty, peliculas_lista):
    if index != -1:
        path, lista = dls(G_studio, size3, index, 1, qty) #no retornar ni peso ni costo solo dejarlo como comentario para que se vea en la expo
        lista.sort(key=return_weight, reverse=True)
        movies_list = return_movies_titles(lista, peliculas_lista)
        return movies_list, path

def filter_selector(movieReference, movieSelectedFilter, movieRecommendationAmount, movie_dataset):
  try:
    index = movie_dataset.index(movieReference)
  except:
    index = -1
    return ["Error, movie not found in the dataset"]
  if movieSelectedFilter == "studio":
    movie_list, path = PC_recomendation(index, movieRecommendationAmount, movie_dataset)
    subgrafo = createSubgraph(G_studio, index)
    drawGraph(subgrafo, quantity=movieRecommendationAmount)
    return movie_list
  elif movieSelectedFilter == "genre":
    movie_list, path = genre_recomendation(index, movieRecommendationAmount, movie_dataset)
    subgrafo = createSubgraph(G_genre, index)
    drawGraph(subgrafo, quantity=movieRecommendationAmount)
    return movie_list
  elif movieSelectedFilter == "overview":
    movie_list, path = overview_recomendation(index, movieRecommendationAmount, movie_dataset)
    subgrafo = createSubgraph(G_overview, index)
    drawGraph(subgrafo, quantity=movieRecommendationAmount)
    return movie_list
  

def drawGraph(L, filename="static/images/graph", quantity=None):
    if os.path.exists(filename):
       os.remove(filename)
    
    graph = gv.Graph("G")
    graph.attr('graph', layout='sfdp')
    graph.attr('node', color='orangered', fontcolor='mediumslateblue', fontname='monospace', fontsize='8', height='0.1', width='0.1')
    graph.attr('edge', color='gray', fontname='monospace', fontsize='8')
    
    nodes = set()
    for i, connection in enumerate(L):
        source, target, weight = connection
        nodes.add(source)
        nodes.add(target)
        
        if i < quantity:
            graph.attr('node', color='orangered', fontcolor='mediumslateblue')
            graph.edge(str(source), str(target), label=str(weight), color='orange', penwidth='2')
        else:
            graph.attr('node', color='black', fontcolor='black')
            graph.edge(str(source), str(target), label=str(weight))
    
    for node in nodes:
        graph.node(str(node), label=str(node))

    try:
      return graph.render(filename, format= "png")
    except:
       return
    
def createSubgraph(graph, source_node, path=[]):
    subgraph = []

    for src, edges in graph.items():
        if src == source_node:
            for dst, weight in edges:
                subgraph.append([src, dst, weight])
    
    orderbyweight(subgraph)
    return subgraph
  
def orderbyweight(subgraph):
  subgraph.sort(key=return_subgraph_weight, reverse=True)

def return_subgraph_weight(e):
  return e[2]