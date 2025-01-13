import pygame
import random
import math

# Clase Nodo para manejar coordenadas y nombre
class Nodo:
    def __init__(self, x, y, nombre):
        self.cor_x = x
        self.cor_y = y
        self.nombre = nombre

# Algoritmo de Fruchterman-Reingold
def fruchterman_reingold(grafo, area, iteraciones=50, t=10):
    nodos = list(grafo.keys())
    k = math.sqrt(area / len(nodos))  # Constante de equilibrio

    for _ in range(iteraciones):
        fuerzas = {nodo: [0, 0] for nodo in nodos}  # Inicializa fuerzas

        # Calcula fuerzas repulsivas
        for i, v in enumerate(nodos):
            for j, u in enumerate(nodos):
                if i != j:
                    dx = v.cor_x - u.cor_x
                    dy = v.cor_y - u.cor_y
                    d = math.sqrt(dx**2 + dy**2) or 0.01  # Evitar división por cero

                    fuerza = -k**2 / d  # Fuerza repulsiva
                    fuerzas[v][0] += (fuerza * dx / d)
                    fuerzas[v][1] += (fuerza * dy / d)

        # Calcula fuerzas atractivas
        for v in nodos:
            for u in grafo[v]:
                dx = v.cor_x - u.cor_x
                dy = v.cor_y - u.cor_y
                d = math.sqrt(dx**2 + dy**2) or 0.01  # Evitar división por cero

                fuerza = d**2 / k  # Fuerza atractiva
                fuerzas[v][0] -= (fuerza * dx / d)
                fuerzas[v][1] -= (fuerza * dy / d)

        # Actualiza posiciones de los nodos
        for nodo in nodos:
            dx, dy = fuerzas[nodo]
            desplazamiento = math.sqrt(dx**2 + dy**2) or 0.01
            nodo.cor_x += (dx / desplazamiento) * min(desplazamiento, t)
            nodo.cor_y += (dy / desplazamiento) * min(desplazamiento, t)

        # Reduce la temperatura (enfriamiento)
        t *= 0.9

# Pygame: Inicialización
pygame.init()
ANCHO, ALTO = 800, 600  # Tamaño reducido de la ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Fruchterman-Reingold Algorithm")
reloj = pygame.time.Clock()

# Generar un grafo con n nodos y conexiones aleatorias
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

# Función para ajustar la escala del grafo dentro de la ventana
def escalar_grafo(grafo):
    min_x = min([nodo.cor_x for nodo in grafo])
    max_x = max([nodo.cor_x for nodo in grafo])
    min_y = min([nodo.cor_y for nodo in grafo])
    max_y = max([nodo.cor_y for nodo in grafo])

    # Calcular el rango de las coordenadas
    rango_x = max_x - min_x
    rango_y = max_y - min_y

    # Factor de escala para que los nodos ocupen más espacio en la ventana
    escala_x = (ANCHO - 100) / rango_x
    escala_y = (ALTO - 100) / rango_y

    # Aplicar la escala
    for nodo in grafo:
        nodo.cor_x = (nodo.cor_x - min_x) * escala_x + 50  # Desplazar para evitar bordes
        nodo.cor_y = (nodo.cor_y - min_y) * escala_y + 50

# Dibujar el grafo
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
        pygame.draw.circle(ventana, (0, 255, 0), (int(nodo.cor_x), int(nodo.cor_y)), 10)  # Nodo más pequeño
        texto = pygame.font.Font(None, 24).render(nodo.nombre, True, (255, 255, 255))
        ventana.blit(texto, (nodo.cor_x + 10, nodo.cor_y - 10))

# Bucle principal
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

        # Ejecuta el algoritmo de Fruchterman-Reingold
        fruchterman_reingold(grafo, area, iteraciones=1)

        # Escala el grafo para ocupar más espacio en la ventana
        escalar_grafo(grafo)

        # Dibuja el grafo
        dibujar_grafo(ventana, grafo)

        # Actualiza la ventana
        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
