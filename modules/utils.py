import random
import pygame
import time
import csv
from modules import settings

def spawn_item(window_x, window_y):
    """
    Genera un elemento en una posición aleatoria dentro de las dimensiones de la ventana.

    Args:
        window_x (int): La anchura de la ventana.
        window_y (int): La altura de la ventana.

    Returns:
        list: Una lista que contiene las coordenadas x e y de la posición de spawn.
    """
    return [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]

def create_obstacles(window_x, window_y, num_obstacles):
    """
    Crea obstáculos generando elementos dentro de las dimensiones de la ventana un número especificado de veces.

    Args:
        window_x (int): La anchura de la ventana.
        window_y (int): La altura de la ventana.
        num_obstacles (int): El número de obstáculos a crear.

    Returns:
        list: Una lista de obstáculos, cada uno representado como una posición de spawn dentro de las dimensiones de la ventana.
    """
    return [spawn_item(window_x, window_y) for _ in range(num_obstacles)]

# def create_moving_enemies(window_x, window_y, num_enemies):
#     """
#     Genera una lista de enemigos en movimiento con posiciones y direcciones aleatorias.

#     Args:
#         window_x (int): La anchura de la ventana.
#         window_y (int): La altura de la ventana.
#         num_enemies (int): El número de enemigos a generar.

#     Returns:
#         list: Una lista de diccionarios que representan a los enemigos en movimiento. Cada diccionario contiene la
#               posición y dirección de un enemigo.
#     """
#     enemies = []
#     for _ in range(num_enemies):
#         enemy = {
#             "position": spawn_item(window_x, window_y),
#             "direction": random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
#         }
#         enemies.append(enemy)
#     return enemies

def validate_direction(change_to, direction):
    """
    Valida la dirección basándose en la entrada change_to y direction.

    Args:
        change_to (str): cambiar_hacia (str): La dirección a la que cambiar. Debe ser una de las siguientes: 'UP', 'DOWN', 'LEFT', o 'RIGHT'.
        direction (str): La dirección actual. Debe ser 'ARRIBA', 'ABAJO', 'IZQUIERDA' o 'DERECHA'.

    Returns:
        str: La dirección validada. Si la dirección change_to es válida y diferente de la dirección actual,
             devuelve la dirección change_to. En caso contrario, devuelve la dirección actual.
    """
    if change_to == 'UP' and direction != 'DOWN':
        return 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        return 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        return 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        return 'RIGHT'
    return direction

def move_player(position, direction):
    """
    Mueve al jugador en la dirección especificada.

    Parameters:
        position (tuple): La posición actual del jugador como una tupla (x, y).
        direction (str): La dirección en la que debe moverse el jugador. Debe ser una de las siguientes: 'ARRIBA', 'ABAJO', 'IZQUIERDA' o 'DERECHA'.
    Returns:
        tuple: La posición actualizada del jugador como una tupla (x, y).
    """
    if direction == 'UP':
        position[1] -= 10
    if direction == 'DOWN':
        position[1] += 10
    if direction == 'LEFT':
        position[0] -= 10
    if direction == 'RIGHT':
        position[0] += 10
    return position

def check_collision(position, window_x, window_y):
    """
    Comprueba si la posición dada colisiona con los límites de la ventana.

    Parameters:
        position (tupla): La posición actual del objeto como una tupla (x, y).
        window_x (int): La anchura de la ventana.
        window_y (int): La altura de la ventana.

    Returns:
        bool: True si la posición colisiona con los límites de la ventana, False en caso contrario.
    """
    # -10 porque considera el cuerpo del jugador a la hora de determinar la colisión
    if position[0] < 0 or position[0] > window_x - 10:
        return True
    if position[1] < 0 or position[1] > window_y - 10:
        return True
    return False

def lose_life(sound, lives):
    """
    Reduce el número de vidas en 1 y reproduce un efecto de sonido.

    Parameters:
        sound: El objeto de sonido utilizado para reproducir un efecto de sonido.
        lives: El número actual de vidas.

    Returns:
        int: El número actualizado de vidas después de decrementar en 1.
    """
    sound.play()
    lives -= 1
    return lives

def display_game_over(game_window, score, window_x, window_y):
    """
    Muestra la pantalla de fin de partida con la puntuación del jugador.

    Parameters:
        game_window: La superficie de la ventana donde se mostrará la pantalla de finalización del juego.
        score: La puntuación del jugador que se mostrará en la pantalla.
        window_x: La anchura de la ventana.
        window_y: La altura de la ventana.

    Returns:
        None
    """
    font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = font.render('Your Score is : ' + str(score), True, (255, 255, 255))
    game_over_rect = game_over_surface.get_rect(center=(window_x / 2, window_y / 2))
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    save_score(get_random_player_name(), score)
    time.sleep(4)
    pygame.quit()
    quit()

def save_score(player_name, score, filename='scores.csv'):
    """
    Guarda la puntuación del jugador en un archivo CSV.

    Args:
        player_name (str): El nombre del jugador.
        score (int): La puntuación del jugador.
        filename (str, optional): El nombre del archivo CSV para guardar la puntuación. Por defecto es 'puntuaciones.csv'.

    Returns:
        None
    """
    # Append mode para agregar datos al archivo, mantiene el contenido existente sin sobreescribirlo
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([player_name, score])

def get_random_player_name():
    """
    Devuelve un nombre aleatorio de la lista predefinida de nombres de jugadores.
    """
    return random.choice(settings.player_names)
