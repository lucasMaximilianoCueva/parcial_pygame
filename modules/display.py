import pygame
from modules import settings

def show_score(window, score, color, font, size):
    """
    Renderiza la partitura en la superficie de la ventana dada.

    Args:
        window (pygame.Surface): La superficie sobre la que dibujar la partitura.
        score (int): La puntuación que se mostrará.
        color (tuple): El color RGB del texto de la partitura.
        font (str): El nombre de la fuente que se utilizará para el texto de la partitura.
        size (int): El tamaño de la fuente que se utilizará para el texto de la partitura.

    Returns:
        None
    """
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    window.blit(score_surface, score_rect)

def show_lives(window, lives, color, font, size, window_x):
    """
    Renderiza el número de vidas en la superficie de la ventana.

    Parameters:
        window: La superficie de la ventana para renderizar las vidas.
        lives: El número de vidas a mostrar.
        color: El color del texto.
        font: El estilo de letra del texto.
        size: El tamaño de letra del texto.
        window_x: La coordenada x de la ventana.

    Returns:
        None
    """
    lives_font = pygame.font.SysFont(font, size)
    lives_surface = lives_font.render('Lives : ' + str(lives), True, color)
    lives_rect = lives_surface.get_rect(topleft=(window_x - 150, 0))
    window.blit(lives_surface, lives_rect)

def start_screen(window, window_x, window_y, background_image_menu):
    """
    Muestra continuamente la pantalla de inicio con diferentes botones en la ventana.
    
    Args:
        window: La superficie sobre la que se dibujará la pantalla de inicio.
        window_x: La anchura de la ventana.
        window_y: La altura de la ventana.
        background_image_menu: La imagen de fondo del menú.
    
    Returns:
        None
    """
    while True:
        window.fill((0, 0, 0))
        window.blit(background_image_menu, [0, 0])
        title_font = pygame.font.SysFont('times new roman', 50)
        button_font = pygame.font.SysFont('times new roman', 35)

        play_button_surface = button_font.render('Play', True, (255, 255, 255))
        play_button_rect = play_button_surface.get_rect(center=(window_x/2, window_y/2))
        window.blit(play_button_surface, play_button_rect)

        options_button_surface = button_font.render('Options', True, (255, 255, 255))
        options_button_rect = options_button_surface.get_rect(center=(window_x/2, window_y/2 + 50))
        window.blit(options_button_surface, options_button_rect)

        scores_button_surface = button_font.render('Scores', True, (255, 255, 255))
        scores_button_rect = scores_button_surface.get_rect(center=(window_x/2, window_y/2 + 100))
        window.blit(scores_button_surface, scores_button_rect)

        quit_button_surface = button_font.render('Quit', True, (255, 255, 255))
        quit_button_rect = quit_button_surface.get_rect(center=(window_x/2, window_y/2 + 150))
        window.blit(quit_button_surface, quit_button_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    return
                elif options_button_rect.collidepoint(mouse_pos):
                    return options_screen(window, window_x, window_y, background_image_menu)
                elif scores_button_rect.collidepoint(mouse_pos):
                    return scores_screen(window, window_x, window_y, background_image_menu)
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

def options_screen(window, window_x, window_y, background_image_menu):
    """
    Muestra continuamente la pantalla de opciones con diferentes botones en la ventana.

    Args:
        window (pygame.Surface): La superficie sobre la que se dibujará la pantalla de opciones.
        window_x (int): La anchura de la ventana.
        window_y (int): La altura de la ventana.
        background_image_menu (pygame.Surface): La imagen de fondo del menú.

    Returns:
        None
    """
    while True:
        window.fill((0, 0, 0))
        options_font = pygame.font.SysFont('times new roman', 50)
        button_font = pygame.font.SysFont('times new roman', 35)

        options_surface = options_font.render('Options', True, (0, 255, 0))
        options_rect = options_surface.get_rect(center=(window_x/2, window_y/4))
        window.blit(options_surface, options_rect)

        easy_button_surface = button_font.render('Easy', True, (255, 255, 255))
        easy_button_rect = easy_button_surface.get_rect(center=(window_x/2, window_y/2))
        window.blit(easy_button_surface, easy_button_rect)

        medium_button_surface = button_font.render('Medium', True, (255, 255, 255))
        medium_button_rect = medium_button_surface.get_rect(center=(window_x/2, window_y/2 + 50))
        window.blit(medium_button_surface, medium_button_rect)

        hard_button_surface = button_font.render('Hard', True, (255, 255, 255))
        hard_button_rect = hard_button_surface.get_rect(center=(window_x/2, window_y/2 + 100))
        window.blit(hard_button_surface, hard_button_rect)

        back_button_surface = button_font.render('Back', True, (255, 255, 255))
        back_button_rect = back_button_surface.get_rect(center=(window_x/2, window_y/2 + 150))
        window.blit(back_button_surface, back_button_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_button_rect.collidepoint(mouse_pos):
                    update_game_settings('easy')
                    return
                elif medium_button_rect.collidepoint(mouse_pos):
                    update_game_settings('medium')
                    return
                elif hard_button_rect.collidepoint(mouse_pos):
                    update_game_settings('hard')
                    return
                elif back_button_rect.collidepoint(mouse_pos):
                    start_screen(window, window_x, window_y, background_image_menu)
                    return

def update_game_settings(difficulty):
    """
    Actualiza la configuración del juego en función del nivel de dificultad especificado.

    Args:
        dificultad (str): El nivel de dificultad con el que actualizar la configuración del juego.

    Returns:
        None

    Esta función actualiza la variable global `config` llamando a la función `update_settings` del módulo `settings`.
    La función `update_settings` toma el parámetro `difficulty` y actualiza la configuración del juego en consecuencia.
    """
    global config
    config = settings.update_settings(difficulty)

import csv

def load_scores(filename='scores.csv'):
    """
    Cargar puntuaciones desde un archivo CSV.

    Esta función lee las puntuaciones de un archivo CSV y devuelve una lista de tuplas, donde cada tupla contiene el nombre del jugador y la puntuación.
    Si el archivo no existe, se devuelve una lista vacía.

    Parameters:
        filename (str): El nombre del archivo CSV para cargar las puntuaciones. Por defecto es 'scores.csv'.

    Returns:
        list: Una lista de tuplas, donde cada tupla contiene el nombre del jugador y la puntuación.
    """
    scores = []
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            # Por cada fila, se crea una tupla con el primer elemento (string) y el segundo (int)
            scores = [(row[0], int(row[1])) for row in reader]
    except FileNotFoundError:
        pass
    return scores

def scores_screen(window, window_x, window_y, background_image_menu):
    """
    Muestra la pantalla de resultados en un partido.

    Args:
        window (pygame.Surface): La superficie sobre la que se dibujará la pantalla de puntuaciones.
        window_x (int): La anchura de la ventana.
        window_y (int): La altura de la ventana.
        background_image_menu (pygame.Surface): La imagen de fondo del menú.

    Returns:
        None
    """
    while True:
        window.fill((0, 0, 0))
        window.blit(background_image_menu, [0, 0])
        scores_font = pygame.font.SysFont('times new roman', 50)
        button_font = pygame.font.SysFont('times new roman', 35)

        scores_surface = scores_font.render('Scores', True, (0, 255, 0))
        scores_rect = scores_surface.get_rect(center=(window_x/2, window_y/4))
        window.blit(scores_surface, scores_rect)

        scores = load_scores()
        y_offset = window_y/4 + 50
        for player_name, score in scores:
            score_text = button_font.render(f'{player_name}: {score}', True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(window_x/2, y_offset))
            window.blit(score_text, score_rect)
            y_offset += 40

        back_button_surface = button_font.render('Back', True, (255, 255, 255))
        back_button_rect = back_button_surface.get_rect(center=(window_x/2, window_y - 50))
        window.blit(back_button_surface, back_button_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(mouse_pos):
                    start_screen(window, window_x, window_y, background_image_menu)
                    return
