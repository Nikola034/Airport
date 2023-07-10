import ast
from datetime import datetime, date, timedelta, time
import csv
from common import konstante

import letovi.letovi

"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
Ova funkcija sluzi samo za prikaz
"""
def pregled_nerealizovanih_letova(svi_letovi: dict):
    lista = []
    for let in svi_letovi:
        if svi_letovi[let]["datum_pocetka_operativnosti"] <= datetime.now():
            continue
        lista.append(svi_letovi[let])
    return lista
"""
Funkcija koja omogucava pretragu leta po yadatim kriterijumima. Korisnik moze da zada jedan ili vise kriterijuma.
Povratna vrednost je lista konkretnih letova.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
"""
def pretraga_letova(svi_letovi: dict, konkretni_letovi:dict, polaziste: str = "", odrediste: str = "",
                    datum_polaska: datetime = None, datum_dolaska: datetime = None,
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "") -> list:
    povratna_lista = []
    for k in konkretni_letovi:
        svaki_let = svi_letovi[konkretni_letovi[k]["broj_leta"]]
        if polaziste != "" and polaziste != None and svaki_let["sifra_polazisnog_aerodroma"] != polaziste:
            continue
        if odrediste != "" and odrediste != None and svaki_let["sifra_odredisnog_aerodorma"] != odrediste:
            continue
        if datum_polaska != None and (konkretni_letovi[k]["datum_i_vreme_polaska"].year != datum_polaska.year or konkretni_letovi[k]["datum_i_vreme_polaska"].month != datum_polaska.month or konkretni_letovi[k]["datum_i_vreme_polaska"].day != datum_polaska.day):
            continue
        if datum_dolaska != None and (konkretni_letovi[k]["datum_i_vreme_dolaska"].year != datum_dolaska.year or konkretni_letovi[k]["datum_i_vreme_dolaska"].month != datum_dolaska.month or konkretni_letovi[k]["datum_i_vreme_dolaska"].day != datum_dolaska.day):
            continue
        if vreme_poletanja != "" and svaki_let["vreme_poletanja"] != vreme_poletanja:
            continue
        if vreme_sletanja != "" and svaki_let["vreme_sletanja"] != vreme_sletanja:
            continue
        if prevoznik != "" and svaki_let["prevoznik"] != prevoznik:
            continue
        povratna_lista.append(konkretni_letovi[k])
    return povratna_lista

"""
Funkcija koja kreira novi rečnik koji predstavlja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova proširenu novim letom. 
Ova funkcija proverava i validnost podataka o letu. Paziti da kada se kreira let, da se kreiraju i njegovi konkretni letovi.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def kreiranje_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str,
                     sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float,  datum_pocetka_operativnosti: datetime = None ,
                    datum_kraja_operativnosti: datetime = None):
    if broj_leta not in svi_letovi:
        if len(broj_leta) != 4 or (broj_leta[0] + broj_leta[1]).isalpha() == False or (
                broj_leta[2] + broj_leta[3]).isnumeric() == False:
            raise Exception("Broj leta nije ispravno unet!")
    else:
        raise Exception("Uneti broj leta vec postoji!")
    if not model:
        raise Exception("Pogresno unet model!")
    if not dani:
        raise Exception("Pogresno uneti dani!")
    if isinstance(vreme_poletanja, str) and vreme_poletanja.count(":") == 1:
        pom = vreme_poletanja.split(":")
        if pom[0].isnumeric() and pom[1].isnumeric():
            pass
        else:
            raise Exception("Pogresno uneto vreme poletanja")
    else:
        raise Exception("Pogresno uneto vreme poletanja")
    if isinstance(vreme_sletanja, str) and vreme_sletanja.count(":") == 1:
        pom = vreme_sletanja.split(":")
        if pom[0].isnumeric() and pom[1].isnumeric():
            pass
        else:
            raise Exception("Pogresno uneto vreme sletanja")
    else:
        raise Exception("Pogresno uneto vreme sletanja")
    if datum_kraja_operativnosti < datum_pocetka_operativnosti:
        raise Exception("Pocetak pre kraja")
    if isinstance(cena, float) == False or cena < 0:
        raise Exception("Pogresan unos cene!")
    let = {
        "broj_leta": broj_leta,
        "sifra_polazisnog_aerodroma": sifra_polazisnog_aerodroma,
        "sifra_odredisnog_aerodorma": sifra_odredisnog_aerodorma,
        "vreme_poletanja": vreme_poletanja,
        "vreme_sletanja": vreme_sletanja,
        "sletanje_sutra": sletanje_sutra,
        "prevoznik": prevoznik,
        "dani": dani,
        "model": model,
        "cena": cena,
        "datum_pocetka_operativnosti": datum_pocetka_operativnosti,
        "datum_kraja_operativnosti": datum_kraja_operativnosti
    }
    svi_letovi[broj_leta] = let
    return svi_letovi
"""
Funkcija koja menja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova sa promenjenim letom. 
Ova funkcija proverava i validnost podataka o letu.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def izmena_letova(
    svi_letovi : dict,
    broj_leta: str,
    sifra_polazisnog_aerodroma: str,
    sifra_odredisnog_aerodorma: str,
    vreme_poletanja: str,
    vreme_sletanja: str,
    sletanje_sutra: bool,
    prevoznik: str,
    dani: list,
    model: dict,
    cena: float,
    datum_pocetka_operativnosti: datetime,
    datum_kraja_operativnosti: datetime
) -> dict:
    if broj_leta not in svi_letovi:
        raise Exception("Uneti broj leta ne postoji!")
    else:
        if len(broj_leta) != 4 or (broj_leta[0] + broj_leta[1]).isalpha() == False or (
                broj_leta[2] + broj_leta[3]).isnumeric() == False:
            raise Exception("Broj leta nije ispravno unet!")
    if not model:
        raise Exception("Pogresno unet model!")
    if not dani:
        raise Exception("Pogresno uneti dani!")
    if not isinstance(sifra_polazisnog_aerodroma, str) or len(sifra_polazisnog_aerodroma) != 3:
        raise Exception("Pogresno polaziste!")
    if not isinstance(sifra_odredisnog_aerodorma, str) or len(sifra_odredisnog_aerodorma) != 3:
        raise Exception("Pogresno odrediste!")
    if not isinstance(prevoznik, str) or prevoznik == "":
        raise Exception("Pogresan prevoznik!")
    if not isinstance(sletanje_sutra, bool):
        raise Exception("Pogresno unet parametar sletanje sutra!")
    if isinstance(vreme_poletanja, str) and vreme_poletanja.count(":") == 1:
        pom = vreme_poletanja.split(":")
        if pom[0].isnumeric() and pom[1].isnumeric():
            pass
        else:
            raise Exception("Pogresno uneto vreme poletanja")
    else:
        raise Exception("Pogresno uneto vreme poletanja")
    if isinstance(vreme_sletanja, str) and vreme_sletanja.count(":") == 1:
        pom = vreme_sletanja.split(":")
        if pom[0].isnumeric() and pom[1].isnumeric():
            pass
        else:
            raise Exception("Pogresno uneto vreme sletanja")
    else:
        raise Exception("Pogresno uneto vreme sletanja")
    if isinstance(cena, float) == False or cena < 0:
        raise Exception("Pogresan unos cene!")
    if datum_kraja_operativnosti < datum_pocetka_operativnosti:
        raise Exception("Datum kraja operativnosti je pre pocetka!")
    svi_letovi[broj_leta]["sifra_polazisnog_aerodroma"] = sifra_polazisnog_aerodroma
    svi_letovi[broj_leta]["sifra_odredisnog_aerodorma"] = sifra_odredisnog_aerodorma
    svi_letovi[broj_leta]["vreme_poletanja"] = vreme_poletanja
    svi_letovi[broj_leta]["vreme_sletanja"] = vreme_sletanja
    svi_letovi[broj_leta]["sletanje_sutra"] = sletanje_sutra
    svi_letovi[broj_leta]["prevoznik"] = prevoznik
    svi_letovi[broj_leta]["dani"] = dani
    svi_letovi[broj_leta]["model"] = model
    svi_letovi[broj_leta]["cena"] = cena
    svi_letovi[broj_leta]["datum_pocetka_operativnosti"] = datum_pocetka_operativnosti
    svi_letovi[broj_leta]["datum_kraja_operativnosti"] = datum_kraja_operativnosti
    return svi_letovi
"""
Funkcija koja cuva sve letove na zadatoj putanji
"""
def sacuvaj_letove(putanja: str, separator: str, svi_letovi: dict):
    with open(putanja, 'w', newline='') as file:
        polja = ("broj_leta", "sifra_polazisnog_aerodroma", "sifra_odredisnog_aerodorma", "vreme_poletanja", "vreme_sletanja", "sletanje_sutra", "prevoznik",
        "dani", "model", "cena", "datum_pocetka_operativnosti", "datum_kraja_operativnosti")
        writer = csv.DictWriter(file, polja, delimiter=separator)
        for let in svi_letovi:
            writer.writerow(svi_letovi[let])
        file.close()

"""
Funkcija koja učitava sve letove iz fajla i vraća ih u rečniku.
"""
def ucitaj_letove_iz_fajla(putanja: str, separator: str) -> dict:
    with open(putanja, 'r', newline='') as file:
        polja = ("broj_leta", "sifra_polazisnog_aerodroma", "sifra_odredisnog_aerodorma", "vreme_poletanja", "vreme_sletanja", "sletanje_sutra", "prevoznik",
        "dani", "model", "cena", "datum_pocetka_operativnosti", "datum_kraja_operativnosti")
        reader = csv.DictReader(file, polja, delimiter=separator)
        svi_letovi = {}
        for row in reader:
            if row["sletanje_sutra"] == "False":
                row["sletanje_sutra"] = False
            else:
                row["sletanje_sutra"] = True
            row["cena"] = float(row["cena"])
            row["dani"] = ast.literal_eval(row["dani"])
            row["model"] = ast.literal_eval(row["model"])
            row["datum_pocetka_operativnosti"] = datetime.strptime(row["datum_pocetka_operativnosti"], "%Y-%m-%d %H:%M:%S")
            row["datum_kraja_operativnosti"] = datetime.strptime(row["datum_kraja_operativnosti"], "%Y-%m-%d %H:%M:%S")
            svi_letovi[row["broj_leta"]] = row
        file.close()
        return svi_letovi

"""
Pomoćna funkcija koja podešava matricu zauzetosti leta tako da sva mesta budu slobodna.
Prolazi kroz sve redove i sve poziciej sedišta i postavlja ih na "nezauzeto".
"""
def podesi_matricu_zauzetosti(svi_letovi: dict, konkretni_let: dict):
    returnLista = []
    model_aviona = svi_letovi[konkretni_let["broj_leta"]]["model"]
    broj_redova = model_aviona["broj_redova"]
    pozicije_sedista = model_aviona["pozicije_sedista"]

    for i in range(0, broj_redova):
        row = []
        for j in range(0, len(pozicije_sedista)):
            row.append(False)
        returnLista.append(row)

    konkretni_let["zauzetost"] = returnLista
    return returnLista


"""
Funkcija koja vraća matricu zauzetosti sedišta. Svaka stavka sadrži oznaku pozicije i oznaku reda.
Primer: [[True, False], [False, True]] -> A1 i B2 su zauzeti, A2 i B1 su slobodni
"""
def matrica_zauzetosti(konkretni_let: dict) -> list:
    return konkretni_let["zauzetost"]


"""
Funkcija koja zauzima sedište na datoj poziciji u redu, najkasnije 48h pre poletanja. Redovi počinju od 1. 
Vraća grešku ako se sedište ne može zauzeti iz bilo kog razloga.
"""
def checkin(karta, svi_letovi: dict, konkretni_let: dict, red: int, pozicija: str) -> (dict, dict):

    if red > svi_letovi[konkretni_let["broj_leta"]]["model"]["broj_redova"] or red < 1:
        raise Exception("Pogresan broj reda!")
    zauzetost = letovi.letovi.matrica_zauzetosti(konkretni_let)
    karta["sediste"] = pozicija + str(red)
    pozicija = ord(pozicija) - 65
    if pozicija < 0:
        raise Exception("Pogresna pozicija!")
    if zauzetost[red-1][pozicija] == True:
        raise Exception("Mesto je zauzeto!")
    else:
        zauzetost[red-1][pozicija] = True
    max_vreme = konkretni_let["datum_i_vreme_polaska"] - timedelta(hours=48)
    if datetime.now() > max_vreme:
        print("Zakasnili ste sa prijavom!")
        raise Exception("Zakasnili ste sa prijavom!")
    konkretni_let["zauzetost"] = zauzetost
    karta["status"] = konstante.STATUS_REALIZOVANA_KARTA
    return (konkretni_let, karta)


"""
Funkcija koja vraća listu konkretni letova koji zadovoljavaju sledeće uslove:
1. Polazište im je jednako odredištu prosleđenog konkretnog leta
2. Vreme i mesto poletanja im je najviše 120 minuta nakon sletanja konkretnog leta
"""
def povezani_letovi(svi_letovi: dict, svi_konkretni_letovi: dict, konkretni_let: dict) -> list:
    povezani = []

    for let in svi_konkretni_letovi:
        svaki_let = svi_letovi[svi_konkretni_letovi[let]["broj_leta"]]
        prosledjen_let = svi_letovi[konkretni_let["broj_leta"]]
        vreme_poletanja = konkretni_let["datum_i_vreme_dolaska"] + timedelta(minutes=120)
        if svaki_let["sifra_polazisnog_aerodroma"] == prosledjen_let["sifra_odredisnog_aerodorma"] and svi_konkretni_letovi[let]["datum_i_vreme_polaska"] <= vreme_poletanja:
            povezani.append(svi_konkretni_letovi[let])
    return povezani

"""
Funkcija koja vraća sve konkretne letove čije je vreme polaska u zadatom opsegu, +/- zadati broj fleksibilnih dana
"""
def fleksibilni_polasci(svi_letovi: dict, konkretni_letovi: dict, polaziste: str, odrediste: str,
                        datum_polaska: date, broj_fleksibilnih_dana: int, datum_dolaska: date) -> list:
    if not isinstance(polaziste, str):
        raise Exception("Pogresno uneto polaziste!")
    if not isinstance(odrediste, str):
        raise Exception("Pogresno uneto odrediste!")
    if not isinstance(broj_fleksibilnih_dana, int):
        raise Exception("Pogresno unet broj fleksibilnih dana!")
    donja_p = datum_polaska - timedelta(days=broj_fleksibilnih_dana)
    gornja_p = datum_polaska + timedelta(days=broj_fleksibilnih_dana)
    lista = []
    for let in konkretni_letovi:
        if konkretni_letovi[let]["broj_leta"] in svi_letovi:
            if svi_letovi[konkretni_letovi[let]["broj_leta"]]["sifra_polazisnog_aerodroma"] == polaziste and svi_letovi[konkretni_letovi[let]["broj_leta"]]["sifra_odredisnog_aerodorma"] == odrediste:
                if donja_p <= konkretni_letovi[let]["datum_i_vreme_polaska"] <= gornja_p:
                        lista.append(konkretni_letovi[let])
    return lista

def trazenje_10_najjeftinijih_letova(svi_letovi: dict, polaziste: str, odrediste: str) -> list:
    if not isinstance(polaziste, str):
        raise Exception("Pogresno uneto polaziste!")
    if not isinstance(odrediste, str):
        raise Exception("Pogresno uneto odrediste!")
    lista = []
    for let in svi_letovi:
        if polaziste != "" and svi_letovi[let]["sifra_polazisnog_aerodroma"] != polaziste:
            continue
        if odrediste != "" and svi_letovi[let]["sifra_odredisnog_aerodorma"] != odrediste:
            continue
        lista.append(svi_letovi[let])
    lista = sorted(lista, key = lambda x: x["cena"])
    top10 = []
    for i in range(len(lista)):
        if i > 9:
            break
        top10.append(lista[i])
    top10 = sorted(top10, key=lambda x: x["cena"], reverse=True)
    return top10