import pygame
import random
import math


class Nodo:
    def __init__(self, x, y, nombre):
        self.cor_x = x
        self.cor_y = y
        self.nombre = nombre


def fruchterman_reingold(grafo, area, iteraciones=50, t=10):
    nodos = list(grafo.keys())
    k = math.sqrt(area / len(nodos))  

    for _ in range(iteraciones):
        fuerzas = {nodo: [0, 0] for nodo in nodos}  

        
        for i, v in enumerate(nodos):
            for j, u in enumerate(nodos):
                if i != j:
                    dx = v.cor_x - u.cor_x
                    dy = v.cor_y - u.cor_y
                    d = math.sqrt(dx**2 + dy**2) or 0.01  

                    fuerza = -k**2 / d  
                    fuerzas[v][0] += (fuerza * dx / d)
                    fuerzas[v][1] += (fuerza * dy / d)

        
        for v in nodos:
            for u in grafo[v]:
                dx = v.cor_x - u.cor_x
                dy = v.cor_y - u.cor_y
                d = math.sqrt(dx**2 + dy**2) or 0.01  

                fuerza = d**2 / k 
                fuerzas[v][0] -= (fuerza * dx / d)
                fuerzas[v][1] -= (fuerza * dy / d)

        
        for nodo in nodos:
            dx, dy = fuerzas[nodo]
            desplazamiento = math.sqrt(dx**2 + dy**2) or 0.01
            nodo.cor_x += (dx / desplazamiento) * min(desplazamiento, t)
            nodo.cor_y += (dy / desplazamiento) * min(desplazamiento, t)

        
        t *= 0.9


pygame.init()
ANCHO, ALTO = 800, 600  
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Fruchterman-Reingold Algorithm")
reloj = pygame.time.Clock()


def generar_grafo(n):
    nodos = []
    grafo = {}

    for i in range(n):
        x = random.randint(100, ANCHO - 100)
        y = random.randint(100, ALTO - 100)
        nodo = Nodo(x, y, f"N{i+1}")
        nodos.append(nodo)

    for nodo in nodos:
        grafo[nodo] = random.sample(nodos, random.randint(1, min(3, n - 1)))

    return grafo


def escalar_grafo(grafo):
    min_x = min([nodo.cor_x for nodo in grafo])
    max_x = max([nodo.cor_x for nodo in grafo])
    min_y = min([nodo.cor_y for nodo in grafo])
    max_y = max([nodo.cor_y for nodo in grafo])

    
    rango_x = max_x - min_x
    rango_y = max_y - min_y

    
    escala_x = (ANCHO - 100) / rango_x
    escala_y = (ALTO - 100) / rango_y

    
    for nodo in grafo:
        nodo.cor_x = (nodo.cor_x - min_x) * escala_x + 50  
        nodo.cor_y = (nodo.cor_y - min_y) * escala_y + 50


def dibujar_grafo(ventana, grafo):
    ventana.fill((0, 0, 0))  # Fondo negro
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
    area = ANCHO * ALTO
    iteraciones = 100
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        
        fruchterman_reingold(grafo, area, iteraciones=1)

        
        escalar_grafo(grafo)

        
        dibujar_grafo(ventana, grafo)

        
        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
