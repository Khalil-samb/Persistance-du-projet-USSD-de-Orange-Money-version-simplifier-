    # Acheter un forfait
    # Effectuer un transfert
    # Annuler le dernier transfert
    # Voir l’historique des transactions
    # Quitter
import re
import json
import os

solde_compte = {"solde" : 10000}
dernier_transfert = None
code_secret = 1234

historique_transactions = []



fichier_path = "ussd.json"

historique_path = "historique.json"


def sauvegarder():
    global solde_compte
    with open(fichier_path, "w") as fichier:
        json.dump(solde_compte, fichier, indent=4)

def charger_le_solde():
    """charger le solde du compte depuis le fichier json"""
    global solde_compte
    if os.path.exists(fichier_path):
        try:
            with open(fichier_path, "r") as fichier:
                solde_compte = json.load(fichier)
        except json.JSONDecodeError:
            print("Fichier corrompu, réinitialisation...")
            solde_compte = {"solde": 10000}
    else:
        solde_compte = {"solde": 10000}
    return solde_compte['solde']


def afficher_solde():
    global solde_compte
    print(f"Solde actuel: {solde_compte['solde']}")

def modifier_solde(montant):
    global solde_compte
    solde_compte['solde'] += montant
    sauvegarder()

# 2ém partie pour historique méme demarche

def sauvegarde_historique():
    """Enregister l'historique des transactions"""
    global historique_transactions
    
    with open(historique_path, "w", encoding="utf-8") as fichier:
        json.dump(historique_transactions, fichier, indent=4)

def charger_historique():
    global historique_transactions
    global historique_path

    if os.path.exists(historique_path):
        try:
            with open(historique_path, "r") as fichier:
                historique_transactions = json.load(fichier)
        except json.JSONDecodeError:
            print("fichier historique mal formé ou il y'a des erreurs")
        except FileNotFoundError:
            print("le fichier n'existe pas ")
    else:
        historique_path = "historique.json"

def retour():

    """Affichage des options de retour"""

    print('-' *20)
    print("9. Acceuil")
    print("0. Précedent")
    
def code_ussd():
    """Vérification du code USSD"""
    code_secret = input("Entez le code USSD pour accéder au menu: ")
    if code_secret == "#144#":
        menu()
        return True
    
    else:
        print("code secret invalide, réessayer ! ")
        return False

def le_solde_actuel():
    """Affichage du solde actuel"""
    code()
    print('-' *20)
    print(f"\n le sode actuel: {solde_compte['solde']} FCFA")

def code():
    """code de verification pour le propriétaire du compte"""
    global code_secret
    while True:
        code = int(input("Entrez votre code secret: "))
        if code == code_secret:
            print("confirmation effectuer avec succés ! ")
            break
        else:
            print("code incorrect: veuiller réessayer à nouveau")
            
def acheter_credit(solde_compte):
    """Permet d'acheter du crédit télephonique"""
    while True:
        try:
            credits = int(input("Montant du crédit à acheter: "))

            if credits<=0:
                print("le montant doit etre supérieur à 0. ")
                continue
            if credits > solde_compte['solde']:
                print("Solde insuffisant, veuiller recharger votre compte. ")
                return solde_compte['solde']
            print(f"\n Montant credit acheter: {credits} FCFA")
            confirmation = input("Confirmer l'achat ?(1: pour confirmer l'achat) : ").strip()
            if confirmation == "1":
                code()
                solde_compte['solde'] -=credits
                sauvegarder()
                historique_transactions.append(f"Achat de credit: {credits} FCFA")
                sauvegarde_historique()
                print(f"\n Crédit de {credits} FCFA acheté avec succés !!")
                print(f"nouveau solde: {solde_compte['solde']}  FCFA")
                break
            else:
                print("vous avez annuler l'achat!!")
                return solde_compte['solde']
        except ValueError:
            print("veuillez entrer un montant valide. ")
    
def forfaits():
    """Voir les forfaits qui existe"""
    global solde_compte
    print("1. Pass 100 Mo – 500 FCFA")
    print("2. Pass 500 Mo – 1 000 FCFA")
    print("3. Pass 1 Go – 2 000 FCFA")
    retour()
    choix = input("Entrer votre choix: ")
    if choix == "1":
        code()
        print("vous avez acheter le forfait de 500f vous avez 100 Mo: ")
        solde_compte['solde']  = (solde_compte['solde'] - 500)
        sauvegarder()
        historique_transactions.append("forfait 100Mo à 500 FCFA")
        sauvegarde_historique()
        print(f"nouveau solde: {solde_compte['solde']} ")
        

    elif choix == "2":
        code()
        print ("vous avez acheter le forfait de 1000f vous avez 500 Mo:")
        solde_compte['solde'] = (solde_compte['solde'] - 1000)
        sauvegarder()
        historique_transactions.append("forfait 500Mo à 1000 FCFA")
        sauvegarde_historique()
        print(f"nouveau solde: {solde_compte['solde']} ")
        

    elif choix == "3":
        code()
        print ("vous avez acheter le forfait de 2000f vous avez 1 Go:")
        solde_compte['solde']  = (solde_compte['solde']  - 2000)
        sauvegarder()
        historique_transactions.append("forfait 1Go à 2000 FCFA")
        sauvegarde_historique()
        print(f"nouveau solde: {solde_compte['solde']} ")

    elif choix == "0":
        return
    elif choix == "9":
        menu()
    else:
        print("choix incorret: veuiller réessayer à nouveau ")
        return
    
def transfert():
    """Effectuer des transfert vers un autre numéro"""
    global solde_compte
    global dernier_transfert

    while True:
        numero_transfert = input("Entrez le numéro du bénéficiaire: ")
        if re.fullmatch(r"\d{9}",numero_transfert) and numero_transfert.replace(" ","").isnumeric() :
            print(f"Vous voulez envoyer au {numero_transfert}")
            break
        else:
            print("le numéro doit contenir obligatoirement 9 chiffre: réessayer à nouveau")

    while True:
        le_montant = int(input (f"vous souhaiter envoyer au {numero_transfert}, la somme de : "))
        if (solde_compte['solde']  - le_montant) > 0 :

            solde_compte['solde']  -= le_montant
            dernier_transfert = le_montant
            sauvegarder()
            historique_transactions.append(f"Vous aviez fait une transaction de {le_montant} au {numero_transfert}")
            sauvegarde_historique()
            code()
            print(f"Opération réussit: votre nouvelle solde est: {solde_compte['solde']} ")
            break
        else:
            print("compte insufisant: penser à recharger votre compte")
            break
    
def annuler_le_transfert():
    """Annuler la derniere transaction"""
    global dernier_transfert
    global solde_compte 

    while True:
        if dernier_transfert is None:
            print("Aucun transfert effectuer. ")
            break

        else:
            print("1. confirmer")
            print("2. annuler")

            choix = input("\n Veuillez entrer le numéro de votre choix: ")

            if choix == "1":
                code_annulation= int(input("Entrez votre code secret: "))
                if code_annulation == code_secret:
                    solde_compte['solde'] += dernier_transfert
                    sauvegarder()
                    historique_transactions.append(f"Annulation d'une transacation donc le montant est {dernier_transfert}")
                    sauvegarde_historique()
                    print(f"Annulation effectuer avec succés votre solde est {solde_compte['solde']}  ")
                    break
                else:
                    print("Code secret incorrect veuiller réessayer")
                    
            elif choix == "2":
                print("Bravo!! Donner c'est Donner")
                return
            else:
                print("Vous avez annuler la confirmation !!")
                return

def Voir_historique():
    """Affiche l'historique des transactions"""
    print("===== Historique des transactions =====")
    if not historique_transactions:
        print("Aucune transaction enregistrée.")
    else:
        for i, transaction in enumerate(historique_transactions, 1):
            print(f"{i}. {transaction}")
    print("-" * 30)

def menu():
    """Affichage du menu principale"""
    while True:
        print("=======Menu principale=========")
        print("1. Consulter votre solde")
        print("2. Acheter du credit")
        print("3. forfaits")
        print("4. effectuer un transfert")
        print("5. Annuler le dernier transfert")
        print("6. Voir l'historique des transactions")
        print("7. Quitter")

        choix = input("\n Veuillez entrer le numéro de votre choix: ") 
        if choix == "1": 
            le_solde_actuel()
        elif choix == "2": 
            acheter_credit(solde_compte)
        elif choix == "3":
            forfaits()
        elif choix == "4": 
            transfert()
        elif choix =="5":
            annuler_le_transfert()
        elif choix =="6":
            Voir_historique()
        elif choix == "7":
            print("Au-revoir !!")
            break
        else: 
            print("choix invalide: Veuiller réessayer à nouveau  ")


charger_le_solde()
charger_historique()
afficher_solde()
code_ussd()



