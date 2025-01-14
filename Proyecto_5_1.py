import pygame
import random
import math

class Nodo:
    def __init__(self, x, y, nombre):
        self.cor_x = x
        self.cor_y = y
        self.nombre = nombre
        
def resortes(s, alfa=0.01, ka=0.1, kr=0.1, iteraciones=1):
    lista_nodos = list(s.keys())  
    d_min = 0.01  

    for _ in range(iteraciones):  
        lista_p = []  

        for a in lista_nodos:  
            frx, fry = 0, 0  
            
            for b in lista_nodos:  
                if a != b:
                    dx = b.cor_x - a.cor_x
                    dy = b.cor_y - a.cor_y
                    d = max((dx**2 + dy**2)**0.5, d_min)  

                    if next((k for k in s[a] if b == k), None) is None:
                        
                        fr = -kr / (d**2)
                        dir_x, dir_y = dx / d, dy / d  
                    else:
                
                        fr = ka * d
                        dir_x, dir_y = dx / d, dy / d  

                    frx += fr * dir_x
                    fry += fr * dir_y

            nueva_x = a.cor_x + alfa * frx
            nueva_y = a.cor_y + alfa * fry
            lista_p.append((nueva_x, nueva_y))

        
        for idx, nodo in enumerate(lista_nodos):
            nodo.cor_x, nodo.cor_y = lista_p[idx]

    return s


pygame.init()
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Algoritmo de resortes")
reloj = pygame.time.Clock()


def generar_grafo(n):
    nodos = []
    grafo = {}

    
    for i in range(n):
        x = random.randint(50, ANCHO - 50)
        y = random.randint(50, ALTO - 50)
        nodo = Nodo(x, y, f"N{i+1}")
        nodos.append(nodo)

    
    for nodo in nodos:
        grafo[nodo] = random.sample(nodos, random.randint(1, min(3, n - 1)))  

    return grafo


def dibujar_grafo(ventana, grafo):
    ventana.fill((0, 0, 0))  
    
    for nodo, vecinos in grafo.items():
        for vecino in vecinos:
            pygame.draw.line(
                ventana, (255, 255, 255),
                (nodo.cor_x, nodo.cor_y),
                (vecino.cor_x, vecino.cor_y),
                2
            )
    
    for nodo in grafo:
        pygame.draw.circle(ventana, (0, 255, 0), (int(nodo.cor_x), int(nodo.cor_y)), 10)
        texto = pygame.font.Font(None, 24).render(nodo.nombre, True, (255, 255, 255))
        ventana.blit(texto, (nodo.cor_x + 10, nodo.cor_y - 10))


def main():
    n = int(input("Ingresa el número de nodos: "))
    grafo = generar_grafo(n)  
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        
        resortes(grafo, alfa=0.01, ka=0.1, kr=0.1, iteraciones=1)

        
        dibujar_grafo(ventana, grafo)

        
        pygame.display.flip()

        
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
