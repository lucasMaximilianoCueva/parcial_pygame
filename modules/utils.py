import random
import pygame
import time
import csv
from modules import settings

def spawn_item(window_x, window_y):
    """
    Generates a random spawn position within the window dimensions.

    Args:
        window_x (int): The width of the window.
        window_y (int): The height of the window.

    Returns:
        list: A list containing the x and y coordinates of the spawn position.
    """
    return [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]

def create_obstacles(window_x, window_y, num_obstacles):
    """
    Creates obstacles by spawning items within the window dimensions a specified number of times.

    Args:
        window_x (int): The width of the window.
        window_y (int): The height of the window.
        num_obstacles (int): The number of obstacles to create.

    Returns:
        list: A list of obstacles, each represented as a spawn position within the window dimensions.
    """
    return [spawn_item(window_x, window_y) for _ in range(num_obstacles)]

def create_moving_enemies(window_x, window_y, num_enemies):
    """
    Generates a list of moving enemies with random positions and directions.

    Args:
        window_x (int): The width of the game window.
        window_y (int): The height of the game window.
        num_enemies (int): The number of enemies to generate.

    Returns:
        list: A list of dictionaries representing the moving enemies. Each dictionary contains the
              position and direction of an enemy.
    """
    enemies = []
    for _ in range(num_enemies):
        enemy = {
            "position": spawn_item(window_x, window_y),
            "direction": random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        }
        enemies.append(enemy)
    return enemies

def validate_direction(change_to, direction):
    """
    Validates the direction based on the change_to and direction input.

    Args:
        change_to (str): The direction to change to. Must be one of 'UP', 'DOWN', 'LEFT', or 'RIGHT'.
        direction (str): The current direction. Must be one of 'UP', 'DOWN', 'LEFT', or 'RIGHT'.

    Returns:
        str: The validated direction. If the change_to direction is valid and different from the current direction,
             it returns the change_to direction. Otherwise, it returns the current direction.
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
    Moves the player in the specified direction.

    Parameters:
        position (tuple): The current position of the player as a tuple (x, y).
        direction (str): The direction in which the player should move. Must be one of 'UP', 'DOWN', 'LEFT', or 'RIGHT'.

    Returns:
        tuple: The updated position of the player as a tuple (x, y).
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
    if position[0] < 0 or position[0] > window_x - 10:
        return True
    if position[1] < 0 or position[1] > window_y - 10:
        return True
    return False

def move_enemies(enemies, window_x):
    """
    Mueve a los enemigos en función de su dirección actual dentro de la ventana de juego.

    Parameters:
        enemies (list): Una lista de diccionarios que representan a los enemigos con sus posiciones y direcciones.
        window_x (int): La anchura de la ventana de juego.

    Returns:
        list: Una lista de diccionarios que representan las posiciones actualizadas de los enemigos tras el movimiento.
    """
    for enemy in enemies:
        direction = enemy["direction"]
        if direction == 'LEFT':
            enemy["position"][0] -= 10
        if direction == 'RIGHT':
            enemy["position"][0] += 10
        if direction == 'UP':
            enemy["position"][1] -= 10
        if direction == 'DOWN':
            enemy["position"][1] += 10

        if enemy["position"][0] < 0 or enemy["position"][0] > window_x - 10:
            enemy["direction"] = 'RIGHT' if direction == 'LEFT' else 'LEFT'
        if enemy["position"][1] < 0 or enemy["position"][1] > window_x - 10:
            enemy["direction"] = 'DOWN' if direction == 'UP' else 'UP'
    return enemies

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
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([player_name, score])

def get_random_player_name():
    """
    Devuelve un nombre aleatorio de la lista predefinida de nombres de jugadores.
    """
    return random.choice(settings.player_names)