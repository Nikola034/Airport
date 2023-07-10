import ast

from letovi import letovi
from common import konstante
from functools import reduce
from datetime import datetime
import csv

"""
Brojačka promenljiva koja se automatski povećava pri kreiranju nove karte.
"""
sledeci_broj_karte = 1

"""
Kupovina karte proverava da li prosleđeni konkretni let postoji i da li ima slobodnih mesta. U tom slučaju se karta 
dodaje  u kolekciju svih karata. Slobodna mesta se prosleđuju posebno iako su deo konkretnog leta, zbog lakšeg 
testiranja. Baca grešku ako podaci nisu validni.
kwargs moze da prihvati prodavca kao recnik, i datum_prodaje kao datetime
recnik prodavac moze imati id i ulogu
CHECKPOINT 2: kupuje se samo za ulogovanog korisnika i bez povezanih letova.
ODBRANA: moguće je dodati saputnike i odabrati povezane letove. 
"""
def kupovina_karte(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    sifra_konkretnog_leta: int,
    putnici: list,
    slobodna_mesta: list,
    kupac: dict,
    **kwargs
) -> (dict, dict):
    if sifra_konkretnog_leta not in svi_konkretni_letovi:
        raise Exception("Uneti konkretni let ne postoji!")
    if kupac["uloga"] != konstante.ULOGA_KORISNIK:
        raise Exception("Prodavac ne moze da kupi kartu!")
    if kwargs["prodavac"] != None:
        for key in kwargs:
            if kwargs[key]["uloga"] != konstante.ULOGA_PRODAVAC:
                raise Exception("Prodavac mora da proda kartu!")
            break
        prodavac = {"korisnicko_ime": kwargs["prodavac"]}
    else:
        prodavac = {"korisnicko_ime": 0}
    ind = 0
    for i in slobodna_mesta:
        for j in i:
            if j == True:
                continue
            ind = 1
            break
    if ind == 0:
        print("Nema slobodnih mesta!")
        raise Exception("Nema slobodnih mesta!")

    global sledeci_broj_karte
    karta = {
        "broj_karte": sledeci_broj_karte,
        "datum_prodaje": datetime.now(),
        "kupac": kupac,
        "prodavac": prodavac["korisnicko_ime"],
        "obrisana": False,
        "putnici": putnici,
        "sifra_konkretnog_leta": sifra_konkretnog_leta,
        "status": konstante.STATUS_NEREALIZOVANA_KARTA
    }
    sve_karte[sledeci_broj_karte] = karta
    sledeci_broj_karte += 1
    return (karta, sve_karte)

def pregled_nerealizovanaih_karata(korisnik: dict, sve_karte: iter):
    lista = []
    for i in range(len(sve_karte)):
        if sve_karte[i]["putnici"][0]["korisnicko_ime"] == korisnik["korisnicko_ime"] \
                and sve_karte[i]["status"] == konstante.STATUS_NEREALIZOVANA_KARTA:
            lista.append(sve_karte[i])
    return lista


"""
Funkcija menja sve vrednosti karte novim vrednostima. Kao rezultat vraća rečnik sa svim kartama, 
koji sada sadrži izmenu.
"""
def izmena_karte(
    sve_karte: iter,
    svi_konkretni_letovi: iter,
    broj_karte: int,
    nova_sifra_konkretnog_leta: int=None,
    nov_datum_polaska:
    datetime=None,
    sediste=None
) -> dict:
    sve_karte[broj_karte]["sediste"] = sediste
    if nova_sifra_konkretnog_leta != None:
        sve_karte[broj_karte]["sifra_konkretnog_leta"] = nova_sifra_konkretnog_leta
    return sve_karte

"""
 Funkcija brisanja karte se ponaša drugačije u zavisnosti od korisnika:
- Prodavac: karta se označava za brisanje
- Admin/menadžer: karta se trajno briše
Kao rezultat se vraća nova kolekcija svih karata.
"""
def brisanje_karte(korisnik: dict, sve_karte: dict, broj_karte: int) -> dict:
    if korisnik["uloga"] == konstante.ULOGA_PRODAVAC:
        sve_karte[broj_karte]["obrisana"] = True
    elif korisnik["uloga"] == konstante.ULOGA_ADMIN:
        del sve_karte[broj_karte]
    else:
        raise Exception("Pogresna uloga!")
    return sve_karte

"""
Funkcija vraća sve karte koje se poklapaju sa svim zadatim kriterijumima. 
Kriterijum se ne primenjuje ako nije prosleđen.
"""
def pretraga_prodatih_karata(sve_karte: dict, svi_letovi:dict, svi_konkretni_letovi:dict, polaziste: str="",
                             odrediste: str="", datum_polaska: datetime="", datum_dolaska: datetime="",
                             korisnicko_ime_putnika: str="")->list:
    lista = []
    for karta in sve_karte:
        konkretan_let = svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]
        svaki_let = svi_letovi[konkretan_let["broj_leta"]]
        if polaziste != "" and polaziste != None and svaki_let["sifra_polazisnog_aerodroma"] != polaziste:
            continue
        if odrediste != "" and odrediste != None and svaki_let["sifra_odredisnog_aerodorma"] != odrediste:
            continue
        if datum_polaska != None and (konkretan_let["datum_i_vreme_polaska"].year != datum_polaska.year or konkretan_let["datum_i_vreme_polaska"].month != datum_polaska.month or konkretan_let["datum_i_vreme_polaska"].day != datum_polaska.day):
            continue
        if datum_dolaska != None and (konkretan_let["datum_i_vreme_dolaska"].year != datum_dolaska.year or konkretan_let["datum_i_vreme_dolaska"].month != datum_dolaska.month or konkretan_let["datum_i_vreme_dolaska"].day != datum_dolaska.day):
            continue
        if korisnicko_ime_putnika != "" and korisnicko_ime_putnika != None and sve_karte[karta]["putnici"][0]["korisnicko_ime"] != korisnicko_ime_putnika:
            continue
        lista.append(sve_karte[karta])
    return lista

"""
Funkcija čuva sve karte u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_karte(sve_karte: dict, putanja: str, separator: str):
    with open(putanja, 'w', newline='') as file:
        polja = ("broj_karte", "sifra_konkretnog_leta", "kupac", "prodavac", "sediste", "datum_prodaje", "obrisana", "status", "putnici")
        writer = csv.DictWriter(file, fieldnames=polja, delimiter=separator)
        for karta in sve_karte:
            writer.writerow(sve_karte[karta])
        file.close()


"""
Funkcija učitava sve karte iz fajla sa zadate putanje sa zadatim separatorom.
"""
def ucitaj_karte_iz_fajla(putanja: str, separator: str) -> dict:
    with open(putanja, 'r', newline='') as file:
        polja = ("broj_karte", "sifra_konkretnog_leta", "kupac", "prodavac", "sediste", "datum_prodaje", "obrisana", "status", "putnici")
        reader = csv.DictReader(file, fieldnames=polja, delimiter=separator)
        karte = {}
        for row in reader:
            row["broj_karte"] = int(row["broj_karte"])
            row["sifra_konkretnog_leta"] = int(row["sifra_konkretnog_leta"])
            if row["obrisana"] == "True":
                row["obrisana"] = True
            else:
                row["obrisana"] = False
            row["putnici"] = eval(row["putnici"])
            row["kupac"] = eval(row["kupac"])
            row["prodavac"] = eval(row["prodavac"])
            karte[row["broj_karte"]] = row
        file.close()
        return karte

