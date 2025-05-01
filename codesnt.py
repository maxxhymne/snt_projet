import time
from local_armoirecontrol import ArmoireController
from colorama import Fore as f, Back as b, Style as s, init
init(autoreset=True)
import questionary

armoire = ArmoireController.new_armoire_instance()

armoire.eco_time = 7

while True:
    if not armoire.door_state and questionary.confirm("ouvrir la porte ?").ask() == True: # nécessaire pour simulation - remplacer par capteur
        armoire.open_door()
        armoire.lights_on()
        armoire.initialized = False


    if armoire.lights and time.time() - armoire.time_lights_on > armoire.eco_time: #économie d'énergie (7s)
        print('Mode économie d\'énergie')
        armoire.lights_off()
        if questionary.confirm("rallumer les lumières ?").ask() == True:
            armoire.lights_on()
        else:
            armoire.close_door()

    if armoire.door_state and not armoire.initialized:
        armoire.start_ui()
        armoire.initialized = True


    time.sleep(2)
