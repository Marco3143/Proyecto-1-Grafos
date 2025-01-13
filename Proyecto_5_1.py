import pygame
import random
import math

# Clase Nodo para manejar coordenadas y nombre
class Nodo:
    def __init__(self, x, y, nombre):
        self.cor_x = x
        self.cor_y = y
        self.nombre = nombre

# Algoritmo de resortes (tu función mejorada)
def resortes(s, alfa=0.01, ka=0.1, kr=0.1, iteraciones=1):
    lista_nodos = list(s.keys())  # Lista de nodos
    d_min = 0.01  # Distancia mínima para evitar divisiones por cero

    for _ in range(iteraciones):  # Solo una iteración por frame
        lista_p = []  # Lista para almacenar las nuevas posiciones de los nodos

        for a in lista_nodos:  # Recorre cada nodo para calcular fuerzas
            frx, fry = 0, 0  # Inicializa las fuerzas netas en x y y
            
            for b in lista_nodos:  # Calcula fuerzas entre el nodo `a` y todos los demás
                if a != b:
                    dx = b.cor_x - a.cor_x
                    dy = b.cor_y - a.cor_y
                    d = max((dx**2 + dy**2)**0.5, d_min)  # Asegura que d >= d_min

                    if next((k for k in s[a] if b == k), None) is None:
                        # Nodo no conectado -> fuerza repulsiva
                        fr = -kr / (d**2)
                        dir_x, dir_y = dx / d, dy / d  # Dirección de la fuerza repulsiva
                    else:
                        # Nodo conectado -> fuerza atractiva
                        fr = ka * d
                        dir_x, dir_y = dx / d, dy / d  # Dirección de la fuerza atractiva

                    frx += fr * dir_x
                    fry += fr * dir_y

            nueva_x = a.cor_x + alfa * frx
            nueva_y = a.cor_y + alfa * fry
            lista_p.append((nueva_x, nueva_y))

        # Actualiza las posiciones de los nodos
        for idx, nodo in enumerate(lista_nodos):
            nodo.cor_x, nodo.cor_y = lista_p[idx]

    return s

# Pygame: Inicialización
pygame.init()
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Algoritmo de resortes")
reloj = pygame.time.Clock()

# Función para generar un grafo con n nodos aleatorios
def generar_grafo(n):
    nodos = []
    grafo = {}

    # Genera n nodos con posiciones aleatorias
    for i in range(n):
        x = random.randint(50, ANCHO - 50)
        y = random.randint(50, ALTO - 50)
        nodo = Nodo(x, y, f"N{i+1}")
        nodos.append(nodo)

    # Genera conexiones aleatorias (aristas) entre los nodos
    for nodo in nodos:
        grafo[nodo] = random.sample(nodos, random.randint(1, min(3, n - 1)))  # Conecta a 1-3 nodos

    return grafo

# Función para dibujar el grafo
def dibujar_grafo(ventana, grafo):
    ventana.fill((0, 0, 0))  # Fondo negro
    # Dibuja las aristas
    for nodo, vecinos in grafo.items():
        for vecino in vecinos:
            pygame.draw.line(
                ventana, (255, 255, 255),
                (nodo.cor_x, nodo.cor_y),
                (vecino.cor_x, vecino.cor_y),
                2
            )
    # Dibuja los nodos
    for nodo in grafo:
        pygame.draw.circle(ventana, (0, 255, 0), (int(nodo.cor_x), int(nodo.cor_y)), 10)
        texto = pygame.font.Font(None, 24).render(nodo.nombre, True, (255, 255, 255))
        ventana.blit(texto, (nodo.cor_x + 10, nodo.cor_y - 10))

# Bucle principal
def main():
    n = int(input("Ingresa el número de nodos: "))
    grafo = generar_grafo(n)  # Genera un grafo aleatorio con n nodos
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        # Ejecuta el algoritmo de resortes (una iteración por frame)
        resortes(grafo, alfa=0.01, ka=0.1, kr=0.1, iteraciones=1)

        # Dibuja el grafo
        dibujar_grafo(ventana, grafo)

        # Actualiza la ventana
        pygame.display.flip()

        # Control de velocidad de frames
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
