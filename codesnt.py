import time
from local_armoirecontrol import ArmoireController
from colorama import Fore as f, Back as b, Style as s, init
init(autoreset=True)
import questionary

armoire = ArmoireController.new_armoire_instance()

while True:
    if not armoire.door_state and questionary.confirm("ouvrir la porte ?").ask() == True: # nécessaire pour simulation
        armoire.open_door()
        armoire.lights_on()


    elif armoire.door_state and armoire.lights and time.time() - armoire.time_lights_on > 7: #économie d'énergie (20s)
        armoire.lights_off()
        print('Mode économie d\'énergie')
        if questionary.confirm("rallumer les lumières ?").ask() == True:
            armoire.lights_on()
        else:
            armoire.close_door()


    time.sleep(2)
