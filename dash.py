from local_armoirecontrol import ArmoireController
from meteo_api import WeatherCache as wc
from local_armoirecontrol import Menus
from colorama import Fore as f, Back as b, Style as s, init
init(autoreset=True)
import questionary
armoire = ArmoireController.new_armoire_instance()


if __name__ == "__main__":
    while True:
        Menus.menu_principal()