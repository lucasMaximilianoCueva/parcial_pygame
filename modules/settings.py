import json

colors = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0)
}

player_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank"]


def load_settings():
    """
    Carga la configuración desde el archivo 'settings.json' y devuelve la configuración como un diccionario.
    """
    with open('settings.json') as config_file:
        return json.load(config_file)
    
def updateJsonFile(settings):
    """
    Una función para actualizar el archivo 'settings.json' con nuevos valores para 'num_obstacles' y 'num_enemies'.
    
    Parameters:
    - settings: Un diccionario que contiene los nuevos valores de 'num_obstacles' y 'num_enemies'.
    
    Returns:
    - None
    """
    with open("settings.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data['num_obstacles'] = settings['num_obstacles']
    data['num_enemies'] = settings['num_enemies']

    with open("settings.json", "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)

def update_settings(difficulty):
    """
    Función que actualiza los ajustes en función del nivel de dificultad especificado.

    Parameters:
    - difficulty: Cadena que indica el nivel de dificultad.

    Returns:
    - None
    """
    with open('settings.json') as config_file:
        settings = json.load(config_file)
        settings['num_obstacles'] = settings['difficulties'][difficulty]['num_obstacles']
        settings['num_enemies'] = settings['difficulties'][difficulty]['num_enemies']
        updateJsonFile(settings)
