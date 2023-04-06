#-- coding: utf-8 --

import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs
from pirc522 import RFID
import time
import requests


ATTENDANCE_URL = 'http://192.168.1.63:3002/attend/new-attend-test?'

GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
GPIO.setwarnings(False) #On désactive les messages d'alerte

rc522 = RFID() #On instancie la lib
RID = [208, 194, 117, 77, 42]
print('ctrl + c')
#On va faire une boucle infinie pour lire en boucle
while True :
    rc522.wait_for_tag() #On attnd qu'une puce RFID passe à portée
    (error, tag_type) = rc522.request() #Quand une puce a été lue, on récupère ses infos

    if not error : #Si on a pas d'erreur
        (error, uid) = rc522.anticoll() #On nettoie les possibles collisions, ça arrive si plusieurs cartes passent en même temps
        

        if not error : #Si on a réussi à nettoyer
            print('id : {}'.format(uid))
            response = requests.get(ATTENDANCE_URL + 'cardId=' + ''.join(map(str, uid)) + '&time=1680518460000&classroom=3-23')
            response_json = response.json()
            print(response_json)
            print('tag_type {}'.format(tag_type))
            if uid == RID:
                print('Success')
            time.sleep(1) #On attend 1 seconde pour ne pas lire le tag des centaines de fois en quelques milli-secondes
