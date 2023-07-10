import ast
import csv

id = 0
"""
Funkcija kreira novi rečnik za model aviona i dodaje ga u rečnik svih modela aviona.
Kao rezultat vraća rečnik svih modela aviona sa novim modelom.
"""
def kreiranje_modela_aviona(
    svi_modeli_aviona: dict,
    naziv: str ="",
    broj_redova: str = "",
    pozicija_sedista: list = []
) -> dict:
    if not isinstance(naziv, str) or naziv == "":
        raise Exception("Pogresan naziv")
    if not isinstance(broj_redova, int):
        raise Exception("Prazan broj redova")
    if not isinstance(pozicija_sedista, list):
        raise Exception("Pogresno uneta pozicija sedista!")
    global id
    model = {
        "id": id,
        "naziv": naziv,
        "broj_redova": broj_redova,
        "pozicije_sedista": pozicija_sedista
    }
    svi_modeli_aviona[id] = model
    id += 1
    return svi_modeli_aviona


"""
Funkcija čuva sve modele aviona u fajl na zadatoj putanji sa zadatim operatorom.
"""
def sacuvaj_modele_aviona(putanja: str, separator: str, svi_aerodromi: dict):
    with open(putanja, 'w', newline='') as file:
        polja = ("id", "naziv", "broj_redova", "pozicije_sedista")
        writer = csv.DictWriter(file, polja, delimiter=separator)
        for model in svi_aerodromi:
            writer.writerow(svi_aerodromi[model])
        file.close()


"""
Funkcija učitava sve modele aviona iz fajla na zadatoj putanji sa zadatim operatorom.
"""
def ucitaj_modele_aviona(putanja: str, separator: str) -> dict:
    with open(putanja, 'r', newline='') as file:
        polja = ("id", "naziv", "broj_redova", "pozicije_sedista")
        reader = csv.DictReader(file, polja, delimiter=separator)
        modeli = {}
        for row in reader:
            row["id"] = int(row["id"])
            row["broj_redova"] = int(row["broj_redova"])
            row["pozicije_sedista"] = ast.literal_eval(row["pozicije_sedista"])
            modeli[row["id"]] = row
    return modeli
