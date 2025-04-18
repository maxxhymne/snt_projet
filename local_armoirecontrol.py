import random
import time
from colorama import Fore as f, Back as b, Style as s, init
init(autoreset=True)
import questionary
from meteo_api import WeatherCache as wc
weather_cache = wc()



class ArmoireController: # toutes les interactions avec l'armoire
    def __init__(self):
        self.door_state = False
        self.lights = False

    def simulate_door(self):
        self.door_state = not self.door_state
    
    def open_door(self):
        self.door_state = True
        print(f"Porte {b.RED}OUVERTE")
        print(f"état var: {self.door_state}")
        
    def close_door(self):
        self.door_state = False
        print(f"{b.GREEN}Porte {f.YELLOW}FERMEE")
        print(f"état var: {self.door_state}")



    def lights_on(self):
        
        self.lights = True
        print(f.YELLOW + "Lumières allumées.")
        self.time_lights_on = time.time()

    def lights_off(self):
        self.lights = False
        print(f.BLUE+"-> Lumières éteintes.")
        
    def show_meteo(self, ccity):
        self.city_meteo_raw = wc.get_weather(weather_cache, ccity)
        print(self.city_meteo_raw)
        
        

    @classmethod
    def new_armoire_instance(cls):
        print("Nouvelle instance d’armoire connectée créée.")
        return cls()

armoire = ArmoireController.new_armoire_instance()


class Menus:
    def menu_principal():
        print(b.RED+s.BRIGHT+"ACTIONS TEST - INTERNAL ONLY")
        choix = questionary.select(
            "choisir:",
            choices=[
                "ouvrir porte",
                "allumer lumière",
                "fermer porte",
                "quitter",
                "récupérer météo",
                "eteindre lumiere"
            ], qmark="🞂"
        ).ask()

        if choix == "allumer lumière":
            armoire.lights_on('all')
        elif choix == "ouvrir porte":
            armoire.open_door()
        elif choix == "fermer porte":
            armoire.close_door()
        elif choix == "quitter":
            exit()
        elif choix == "récupérer météo":
            ch_city = questionary.text("Entrer le nom d'une ville :").ask()
            armoire.show_meteo(ch_city)
        elif choix == "eteindre lumiere":
            armoire.lights_off()
            