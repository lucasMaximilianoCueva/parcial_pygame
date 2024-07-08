import pygame
import time
import random
import json
import csv
from modules import settings, display, utils

try:
    # Inicializar pygame
    pygame.init()

    # Función para cargar la configuración
    def load_game_settings():
        """
        Carga la configuración del juego llamando a la función `load_settings` del módulo `settings`.

        Returns:
            dict: La configuración del juego cargada como diccionario.
        """
        return settings.load_settings()

    # Configuración inicial
    config = load_game_settings()

    # Inicializar ventana del juego
    pygame.display.set_caption('')
    game_window = pygame.display.set_mode((config['window_x'], config['window_y']))

    # Función para cargar y actualizar la configuración después de la pantalla de inicio
    def reload_settings():
        """
        Recarga la configuración del juego y actualiza los obstáculos estáticos y los enemigos en movimiento.

        Esta función recarga la configuración del juego llamando a la función `load_game_settings()`.
        Después actualiza la variable global `config` con los nuevos ajustes.

        Además, llama a las funciones `create_obstacles()` y `create_moving_enemies()` del módulo `utils
        del módulo `utils` para generar nuevos obstáculos estáticos y enemigos en movimiento basados en
        el tamaño actualizado de la ventana y el número de obstáculos y enemigos.

        Parameters:
            None

        Returns:
            None
        """
        global config, static_obstacles, moving_enemies
        config = load_game_settings()
        static_obstacles = utils.create_obstacles(config['window_x'], config['window_y'], config['num_obstacles'])
        moving_enemies = utils.create_moving_enemies(config['window_x'], config['window_y'], config['num_enemies'])

    # Cargar imagen de fondo y sonidos
    background_image = pygame.image.load(config['background_image']).convert()
    background_menu = pygame.image.load(config['background_menu']).convert()
    pygame.mixer.music.load(config['background_music'])
    lose_life_sound = pygame.mixer.Sound(config['lose_life_sound'])
    gem_sound = pygame.mixer.Sound(config['gem_sound'])
    power_up_sound = pygame.mixer.Sound(config['power_up_sound'])

    # Iniciar música de fondo
    pygame.mixer.music.play(-1)

    # Controlador de FPS
    fps = pygame.time.Clock()

    # Posición inicial del jugador
    player_position = [100, 50]
    player_body = [[100, 50]]

    # Posición inicial de la gema y power-up
    gem_position, power_up_position = utils.spawn_item(config['window_x'], config['window_y']), utils.spawn_item(config['window_x'], config['window_y'])
    gem_spawn, power_up_spawn = True, True
    power_up_active, power_up_end_time = False, 0

    # Dirección inicial del jugador
    direction, change_to = 'RIGHT', 'RIGHT'

    # Puntaje inicial
    score, lives = 0, config['initial_lives']

    # Obstáculos y enemigos en movimiento
    static_obstacles = utils.create_obstacles(config['window_x'], config['window_y'], config['num_obstacles'])
    moving_enemies = utils.create_moving_enemies(config['window_x'], config['window_y'], config['num_enemies'])

    # Temporizador de obstáculos
    obstacles_hidden = False
    obstacles_show_time = 0

    # Función principal del juego
    def main():
        """
        La función principal que ejecuta el bucle del juego.

        Esta función inicializa la ventana del juego, carga los ajustes del juego y comienza el bucle del juego.
        Continuamente maneja eventos, actualiza el estado del juego, y renderiza el juego en la pantalla.

        Parameters:
        None

        Returns:
        None

        Efectos secundarios:
        - Inicializa la ventana del juego y establece el título.
        - Carga los ajustes del juego y actualiza la configuración del juego.
        - Inicia el bucle del juego y maneja los eventos, actualizando el estado del juego, y renderizando el juego en la pantalla.

        Raises:
        - pygame.error: Si se produce un error durante el bucle de juego.
        - Excepción: Si hay un error inesperado durante el bucle del juego.
        """
        global player_position, player_body, direction, change_to, score, lives, gem_spawn, gem_position, power_up_spawn, power_up_position, power_up_active, power_up_end_time, moving_enemies, obstacles_hidden, obstacles_show_time

        display.start_screen(game_window, config['window_x'], config['window_y'], background_menu)

        # Cargar la configuración nuevamente después de la pantalla de inicio
        reload_settings()

        while True:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP or event.key == ord('w'):
                            change_to = 'UP'
                        if event.key == pygame.K_DOWN or event.key == ord('s'):
                            change_to = 'DOWN'
                        if event.key == pygame.K_LEFT or event.key == ord('a'):
                            change_to = 'LEFT'
                        if event.key == pygame.K_RIGHT or event.key == ord('d'):
                            change_to = 'RIGHT'

                direction = utils.validate_direction(change_to, direction)
                player_position = utils.move_player(player_position, direction)

                player_body.insert(0, list(player_position))
                if player_position == gem_position:
                    score += 10
                    gem_spawn = False
                    gem_sound.play()
                else:
                    player_body.pop()

                if not gem_spawn:
                    gem_position = utils.spawn_item(config['window_x'], config['window_y'])
                gem_spawn = True

                if power_up_spawn:
                    power_up_position = utils.spawn_item(config['window_x'], config['window_y'])
                    power_up_spawn = False
                    power_up_sound.play()

                if player_position == power_up_position:
                    power_up_active = True
                    power_up_end_time = time.time() + config['power_up_duration']
                    power_up_spawn = True
                    obstacles_hidden = True
                    obstacles_show_time = time.time() + config['power_up_duration']

                if power_up_active and time.time() > power_up_end_time:
                    power_up_active = False

                if obstacles_hidden and time.time() > obstacles_show_time:
                    obstacles_hidden = False

                game_window.fill(settings.colors['black'])
                game_window.blit(background_image, [0, 0])

                for pos in player_body:
                    pygame.draw.rect(game_window, config['player_color'], pygame.Rect(pos[0], pos[1], 10, 10))
                pygame.draw.rect(game_window, settings.colors['white'], pygame.Rect(gem_position[0], gem_position[1], 10, 10))

                if not power_up_spawn:
                    pygame.draw.rect(game_window, settings.colors['yellow'], pygame.Rect(power_up_position[0], power_up_position[1], 10, 10))

                if not obstacles_hidden:
                    for obstacle in static_obstacles:
                        pygame.draw.rect(game_window, settings.colors['red'], pygame.Rect(obstacle[0], obstacle[1], 10, 10))
                        if player_position == obstacle:
                            lives = utils.lose_life(lose_life_sound, lives)
                            if lives == 0:
                                utils.display_game_over(game_window, score, config['window_x'], config['window_y'])

                for enemy in moving_enemies:
                    pygame.draw.rect(game_window, settings.colors['blue'], pygame.Rect(enemy["position"][0], enemy["position"][1], 10, 10))
                    if player_position == enemy["position"]:
                        lives = utils.lose_life(lose_life_sound, lives)
                        if lives == 0:
                            utils.display_game_over(game_window, score, config['window_x'], config['window_y'])

                moving_enemies = utils.move_enemies(moving_enemies, config['window_x'])

                # Loses all lives if player collides with wall
                if utils.check_collision(player_position, config['window_x'], config['window_y']):
                    lose_life_sound.play()
                    utils.display_game_over(game_window, score, config['window_x'], config['window_y'])

                for block in player_body[1:]:
                    if player_position == block:
                        lives = utils.lose_life(lose_life_sound, lives)
                        if lives == 0:
                            utils.display_game_over(game_window, score, config['window_x'], config['window_y'])

                display.show_score(game_window, score, settings.colors['white'], 'times new roman', 20)
                display.show_lives(game_window, lives, settings.colors['white'], 'times new roman', 20, config['window_x'])

                pygame.display.update()
                fps.tick(config['player_speed'])

            except pygame.error as e:
                print(f"Pygame error during game loop: {e}")
                pygame.quit()
                quit()
            except Exception as e:
                print(f"Unexpected error: {e}")
                pygame.quit()
                quit()

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"Error importing modules: {e}")
    quit()
except FileNotFoundError as e:
    print(f"File not found: {e}")
    quit()
except json.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")
    quit()
except csv.Error as e:
    print(f"CSV error: {e}")
    quit()
except KeyError as e:
    print(f"KeyError: {e}")
    quit()
except pygame.error as e:
    print(f"Pygame error: {e}")
    quit()
except Exception as e:
    print(f"Unexpected error: {e}")
    quit()
