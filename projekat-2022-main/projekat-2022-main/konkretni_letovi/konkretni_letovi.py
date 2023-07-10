import ast
from datetime import datetime, timedelta
import csv

import letovi.letovi

"""
Funkcija koja za zadati konkretni let kreira sve konkretne letove u opsegu operativnosti.
Kao rezultat vraća rečnik svih konkretnih letova koji sadrži nove konkretne letove.
"""
def kreiranje_konkretnog_leta(svi_konkretni_letovi: dict, let: dict) -> dict:
    max_sifra = max(svi_konkretni_letovi.keys(), default=0)
    poc = let["datum_pocetka_operativnosti"]
    kraj = let["datum_kraja_operativnosti"]
    sat_poletanja = let['vreme_poletanja'][:2]
    minut_poletanja = let['vreme_poletanja'][3:]
    sat_sletanja = let['vreme_sletanja'][:2]
    minut_sletanja = let['vreme_sletanja'][3:]
    while poc < kraj:
        weekday = poc.weekday()
        if weekday in let["dani"]:
            konkretan_let = {
                "sifra": max_sifra+1,
                "broj_leta": let["broj_leta"],
                "datum_i_vreme_polaska": poc.replace(hour=int(sat_poletanja), minute=int(minut_poletanja)),
                "datum_i_vreme_dolaska": poc.replace(hour=int(sat_sletanja), minute=int(minut_sletanja)),
                "zauzetost": []
            }
            max_sifra += 1
            svi_konkretni_letovi[konkretan_let["sifra"]] = konkretan_let
        poc += timedelta(days=1)
    return svi_konkretni_letovi

"""
Funkcija čuva konkretne letove u fajl na zadatoj putanji sa zadatim separatorom. 
"""
def sacuvaj_kokretan_let(putanja: str, separator: str, svi_konkretni_letovi: dict):
    with open(putanja, 'w', newline='') as file:
        polja = ("sifra", "broj_leta", "datum_i_vreme_polaska", "datum_i_vreme_dolaska", "zauzetost")
        writer = csv.DictWriter(file, polja, delimiter=separator)
        for let in svi_konkretni_letovi:
            writer.writerow(svi_konkretni_letovi[let])
        file.close()


"""
Funkcija učitava konkretne letove iz fajla na zadatoj putanji sa zadatim separatorom.
"""
def ucitaj_konkretan_let(putanja: str, separator: str) -> dict:
    with open(putanja, 'r', newline='') as file:
        polja = ("sifra", "broj_leta", "datum_i_vreme_polaska", "datum_i_vreme_dolaska", "zauzetost")
        reader = csv.DictReader(file, polja, delimiter=separator)
        svi_konkretni_letovi = {}
        for row in reader:
            row["sifra"] = int(row["sifra"])
            row["datum_i_vreme_polaska"] = datetime.strptime(row["datum_i_vreme_polaska"], "%Y-%m-%d %H:%M:%S")
            row["datum_i_vreme_dolaska"] = datetime.strptime(row["datum_i_vreme_dolaska"], "%Y-%m-%d %H:%M:%S")
            row["zauzetost"] = ast.literal_eval(row["zauzetost"])
            svi_konkretni_letovi[row["sifra"]] = row
        file.close()
        return svi_konkretni_letovi
