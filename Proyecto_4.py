import random
import networkx as nx

class Nodo:
    def __init__(self, id):
        self.id = id
        self.peso = 0
        self.lista = []
        self.cor_x = None
        self.cor_y = None

class Arista:
    def __init__(self, origen, destino):
        self.peso = None
        self.origen = origen
        self.destino = destino

class Grafo:
    def __init__(self):
        self.g={}
    
    def Crea_gra_arch(self):
        G = nx.Graph()
        for clave in self.g:
            G.add_node(clave.id)
            for i in range(0,len(self.g[clave])):
                G.add_edge(self.g[clave][i].origen.id, self.g[clave][i].destino.id)
        return G       
    
    def KruskalD(self):
        self.inserta_peso_arista()
        conjunto_1 = set()
        conjunto_2 = set()
        lista_sets = []
        lista_pesos = []
        lista_ari = []
        lista_ari_eli = []
        lista_dordenada = sum(self.g.values(), [])
        for i in lista_dordenada:
            lista_pesos.append(i.peso)
        lista_pesos.sort()
        #print(lista_pesos)
        cont = int(len(lista_pesos)/2)
        for n in range(0,cont):
            del lista_pesos[n]
        for j in lista_pesos:
            lista_ari.append(next(k for k in lista_dordenada if j == k.peso))
        
        for a in lista_ari:
            conjunto_1 = None
            conjunto_2 =None
            for i in lista_sets:
                if a.origen in i and a.destino in i:
                    conjunto_1 = conjunto_2 = i
                    lista_ari_eli.append(next(h for h in self.g[a.destino] if h.destino == a.origen))
                    lista_ari_eli.append(a)
                    break
                elif a.origen in i:
                    conjunto_1 = i
                elif a.destino in i:
                    conjunto_2 = i
                if conjunto_1 and conjunto_2:
                    break

            if conjunto_1 and conjunto_2:
                if conjunto_1 != conjunto_2:
                    conjunto_1.update(conjunto_2)
                    lista_sets.remove(conjunto_2)
            else:
                if not conjunto_1 and not conjunto_2:
                    lista_sets.append({a.origen, a.destino})
                else:
                    if not conjunto_1:
                        conjunto_2.add(a.origen)
                    else:
                        conjunto_1.add(a.destino)
        for e in lista_ari_eli:
            self.g[e.origen].remove(e)
    
    def KruskalI(self):
        self.inserta_peso_arista()
        lista_pesos = []
        lista_ari = []
        lista_v = []
        lista_eli = []
        lista_ocultos = []
        lista_dordenada = sum(self.g.values(), [])
        for i in lista_dordenada:
            lista_pesos.append(i.peso)
        lista_pesos.sort(reverse = True)
        cont = int(len(lista_pesos)/2)
        for n in range(0,cont):
            del lista_pesos[n]
        for j in lista_pesos:
            lista_ari.append(next(k for k in lista_dordenada if j == k.peso))

        for o in lista_ari:
            aux_ari = next(g for g in self.g[o.destino] if o.origen == g.destino)
            lista_v.append(o.origen)
            lista_ocultos.append(o)
            lista_ocultos.append(aux_ari)
            self.BusquedaK(o.origen, lista_ocultos, lista_v)
            #print(lista_eli)
            if set(lista_v) == set(self.g.keys()):
                lista_eli.append(o)
                lista_eli.append(aux_ari)
            else:
                lista_ocultos.remove(o)
                lista_ocultos.remove(aux_ari)
            lista_v = []
        
        for e in lista_eli:
            self.g[e.origen].remove(e)
    
    def BusquedaK(self, np, lo, lv):
        for i in self.g[np]:
            if i not in lo:
                if i.destino not in lv:
                    lv.append(i.destino)
                    self.BusquedaK(i.destino, lo, lv)

    def Prim(self, s):
        self.inserta_peso_arista()
        nodopadre = next((i for i in self.g.keys() if i.id == s),None)
        lista_v = [nodopadre] #Lista de nodos visitados
        lista_t = [nodopadre] #Lista de nodos trabajando
        lista_ari = []
        lista_aux = []
        cant = 0
        while lista_t: #Verifica que la lista_t no este vacia
            for i in lista_t: #Recorre los nodos a trabajar
                for j in self.g[i]: #Recorre los aristas de el nodo, j adquiere el valor de una arista
                    if j.destino not in lista_v: #Verifica que el nodo siguiente este visitado
                        #peso = j.peso
                        if cant == 0 or cant > j.peso:
                            cant = j.peso
                            aux_arist = j
                    else:
                        if next((n for n in self.g[i] if n.destino not in lista_v), None) == None:#Verifica si nodos los nodos ya fueron visitados 
                            lista_aux.append(i)
                            break
            if lista_aux:
                    for e in lista_aux:
                        lista_t.remove(e)
                    lista_aux = []
            if lista_t:
                lista_t.append(aux_arist.destino)
                lista_ari.append((aux_arist.origen.id, aux_arist.destino.id))
                lista_ari.append((aux_arist.destino.id, aux_arist.origen.id))
                lista_v.append(aux_arist.destino)
                cant = 0
                aux_arist = None

        for i in lista_ari:
            print(i)
        for n in self.g.keys():
            for m in self.g[n]:
                if (m.origen.id, m.destino.id) not in lista_ari:
                    lista_aux.append(m)
        for x in lista_aux:
            self.g[x.origen].remove(x)

def Imp_Grafo(gr):
    for clave in gr.g:
        print(f'{clave.id}->', end="")
        for i in gr.g[clave]:
            print(f' [{i.origen.id},{i.destino.id}({i.destino.peso}), {i.peso}]', end="")
        print()

def Genera_lista_nod(n,k):
    l = []
    for i in range(1,n+1):
        aux = Nodo(i)
        if k:
            aux.cor_x = round(random.random(), 2)
            aux.cor_y = round(random.random(), 2)
        l.append(aux)
    random.shuffle(l)
    return l

def veri_data(graf,l,x,y):
    for i in graf.g:
        for j in range(0,len(graf.g[i])):
            if (l[x] == graf.g[i][j].origen and l[y] == graf.g[i][j].destino) or (l[y] == graf.g[i][j].origen and l[x] == graf.g[i][j].destino):
                return False
    return True

def Grafo_Gilbert(n,p):
    l = Genera_lista_nod(n,False)
    graf = Grafo()
    for i in range(0,n):
        for j in range(0,n):
            if i != j:
                if veri_data(graf, l, i , j):
                    proba = round(random.random(),2)
                    if proba <= p:
                        if l[i] in graf.g.keys() and l[j] in graf.g.keys():
                            graf.g[l[i]].append(Arista(l[i],l[j]))
                            graf.g[l[j]].append(Arista(l[j],l[i]))
                        else:
                            if l[i] not in graf.g.keys() and l[j] not in graf.g.keys():
                                graf.g[l[i]] = list([Arista(l[i],l[j])])
                                graf.g[l[j]] = list([Arista(l[j],l[i])])
                            else:
                                if l[i] not in graf.g.keys() and l[j] in graf.g.keys():
                                    graf.g[l[i]] = list([Arista(l[i],l[j])])
                                    graf.g[l[j]].append(Arista(l[j],l[i]))
                                else:
                                    graf.g[l[i]].append(Arista(l[i],l[j]))
                                    graf.g[l[j]] = list([Arista(l[j],l[i])])
    return graf

def Grafo_Erdos_Renyi(n,a):
    graf = Grafo()
    l = Genera_lista_nod(n,False)
    aux = []
    print(len(l))
    for i in range(0,a):
        while True:
            x = random.randint(0,n-1)
            y = random.randint(0,n-1)
            #print(x,y)
            if x != y and veri_data(graf,l,x,y):
                if l[x] in graf.g.keys() and l[y] in graf.g.keys():
                        graf.g[l[x]].append(Arista(l[x],l[y]))
                        graf.g[l[y]].append(Arista(l[y],l[x]))
                        break
                else:
                    if l[x] not in graf.g.keys() and l[y] not in graf.g.keys():
                        graf.g[l[x]] = list([Arista(l[x],l[y])])
                        graf.g[l[y]] = list([Arista(l[y],l[x])])
                        break
                    else:
                        if l[x] not in graf.g.keys() and l[y] in graf.g.keys():
                            graf.g[l[x]] = list([Arista(l[x],l[y])])
                            graf.g[l[y]].append(Arista(l[y],l[x]))
                            break
                        else:
                            graf.g[l[x]].append(Arista(l[x],l[y]))
                            graf.g[l[y]] = list([Arista(l[y],l[x])])
                            break
    return graf

def Barabasi_Albert(n,d):
    graf = Grafo()
    l = Genera_lista_nod(n,False)
    graf.g[l[0]] = list([Arista(l[0],l[1])])
    graf.g[l[1]] = list([Arista(l[1],l[0])])

    for i in range(2,n):
        while l[i] not in graf.g.keys():
            for j in range(len(graf.g)):
                proba = round(random.uniform(0.001,1),3)
                if  proba <= 1-(len(graf.g[l[j]])/d):
                    graf.g[l[i]] = list([Arista(l[i],l[j])])
                    graf.g[l[j]].append(Arista(l[j],l[i]))
                    break
    return graf

def Dorogovtsev_Mendes(n):
    graf = Grafo()
    l = Genera_lista_nod(n,False)
    a = []
    graf.g[l[0]] = list([Arista(l[0],l[1]), Arista(l[0],l[2])])
    graf.g[l[1]] = list([Arista(l[1],l[2]), Arista(l[1],l[0])])
    graf.g[l[2]] = list([Arista(l[2],l[0]), Arista(l[2],l[1])])
    a.append(graf.g[l[0]][0])
    a.append(graf.g[l[1]][0])
    a.append(graf.g[l[2]][0])
    for i in range(3,n):
        x = random.randint(0,len(a)-1)
        graf.g[l[i]] = list([Arista(l[i], a[x].origen),Arista(l[i], a[x].destino)])
        graf.g[a[x].origen].append(Arista(a[x].origen, l[i]))
        graf.g[a[x].destino].append(Arista(a[x].destino, l[i]))
        a.append(graf.g[l[i]][0])
        a.append(graf.g[l[i]][1])
    return graf

def geografico_simple(n,r):
    graf = Grafo()
    l = Genera_lista_nod(n,True)
    for i in range(0,n):
        for j in range(0,n):
            if i != j:
                if abs(((l[i].cor_x-l[j].cor_x)**2)+((l[i].cor_y-l[j].cor_y)**2))<=r:
                    if l[i] in graf.g.keys():
                        graf.g[l[i]].append(Arista(l[i],l[j]))
                    else:
                        graf.g[l[i]] = list([Arista(l[i],l[j])])
    return graf

def graf_Malla(n,m):
    graf = Grafo()
    l = Genera_lista_nod(n*m,False)
    x = len(l)
    graf.g[l[0]] = []
    for i in range(0,x):
        if i+1 < m: 
            graf.g[l[i]].append(Arista(l[i], l[i+1]))
            graf.g[l[i]].append(Arista(l[i], l[i+m]))
            graf.g[l[i+1]] = ([Arista(l[i+1], l[i])])
            graf.g[l[i+m]] = ([Arista(l[i+m], l[i])])
        else:
            if (i+1)%m != 0 and i+1 < x-m:
                graf.g[l[i]].append(Arista(l[i], l[i+1]))
                graf.g[l[i]].append(Arista(l[i], l[i+m]))
                graf.g[l[i+1]].append(Arista(l[i+1], l[i]))
                graf.g[l[i+m]] = ([Arista(l[i+m], l[i])])
            else:
                if (i+1)%m == 0 and i+1 <= x-m:
                    graf.g[l[i]].append(Arista(l[i], l[i+m]))
                    graf.g[l[i+m]] = ([Arista(l[i+m], l[i])]) 
                else:
                    if (i+1)%m != 0 and i+1 > x-m:
                        graf.g[l[i]].append(Arista(l[i], l[i+1]))
                        graf.g[l[i+1]].append(Arista(l[i+1], l[i]))
    return graf
