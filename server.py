# Définition d'un serveur réseau gérant un système de CHAT simplifié.
# Utilise les threads pour gérer les connexions clientes en parallèle.

HOST = "localhost"
PORT = 8000

import socket, sys, threading
import re


class ThreadClient(threading.Thread):
    """dérivation d'un objet thread pour gérer la connexion avec un client"""

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn

    nomClient = ""

    def run(self):
        # Dialogue avec le client :
        # Recuperer le nom du client
        connexion.send("Bienvenu! Choisissez un nom d'utilisateur:  ".encode("utf-8"))
        nomClient = self.connexion.recv(1024).decode("utf-8")
        while not re.search("^[a-zA-Z]+[a-zA-Z0-9]*$", nomClient):
            try:
                connexion.send("entrez un nom valide".encode("utf-8"))
                nomClient = self.connexion.recv(1024).decode("utf-8")
            except:
                pass
        for k, val in conn_client.items():
            if self.connexion == val:
                del conn_client[k]
                conn_client[nomClient] = self.connexion
                break
        connexion.send("Vous etes connecté avec succès".encode("utf-8"))
        print(
            "Client {} connecté, adresse IP {}, port {}.".format(
                nomClient, adresse[0], adresse[1]
            )
        )
        while 1:
            msgClient = self.connexion.recv(1024).decode("utf-8")
            if msgClient.upper() == "FIN" or msgClient == "":
                break
            message = "%s> %s" % (nomClient, msgClient)
            print(message)
            # Faire suivre le message à tous les autres clients :
            for cle in conn_client:
                if cle != nomClient:  # ne pas le renvoyer à l'émetteur
                    conn_client[cle].send(message.encode("utf-8"))
        # Fermeture de la connexion :
        self.connexion.close()  # couper la connexion côté serveur
        del conn_client[nomClient]  # supprimer son entrée dans le dictionnaire
        print("Client %s déconnecté." % nomClient)
        # Le thread se termine ici


# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print("La liaison du socket à l'adresse choisie a échoué.")
    sys.exit()
print("Serveur prêt, en attente de requêtes ...")
mySocket.listen(5)

# Attente et prise en charge des connexions demandées par les clients :
conn_client = {}  # dictionnaire des connexions clients
while 1:
    connexion, adresse = mySocket.accept()
    # Créer un nouvel objet thread pour gérer la connexion :
    th = ThreadClient(connexion)
    th.start()
    # Mémoriser la connexion dans le dictionnaire :
    it = th.name  # identifiant du thread
    conn_client[it] = connexion
