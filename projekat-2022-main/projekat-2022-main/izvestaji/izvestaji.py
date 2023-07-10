from datetime import datetime, date, timedelta
"""
Funkcija kao rezultat vraća listu karata prodatih na zadati dan.
"""
def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: date) -> list:
    lista = []
    for karta in sve_karte:
        if sve_karte[karta]["datum_prodaje"].year == dan.year and sve_karte[karta]["datum_prodaje"].month == dan.month and sve_karte[karta]["datum_prodaje"].day == dan.day:
            lista.append(sve_karte[karta])
    return lista


"""
Funkcija kao rezultat vraća listu svih karata čiji je dan polaska leta na zadati dan.
"""
def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: date) -> list:
    lista = []
    for karta in sve_karte:
        if svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"].year == dan.year and svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"].month == dan.month and svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"].day == dan.day:
            lista.append(sve_karte[karta])
    return lista

"""
Funkcija kao rezultat vraća listu karata koje je na zadati dan prodao zadati prodavac.
"""
def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: date, prodavac: str) -> list:
    lista = []
    for karta in sve_karte:
        if sve_karte[karta]["prodavac"] == prodavac and sve_karte[karta]["datum_prodaje"].year == dan.year and sve_karte[karta]["datum_prodaje"].month == dan.month and sve_karte[karta]["datum_prodaje"].day == dan.day:
            lista.append(sve_karte[karta])
    return lista

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata prodatih na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_prodaje(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi,
    dan: date
) -> tuple:
    broj = cena = 0
    for karta in sve_karte:
        if sve_karte[karta][
            "datum_prodaje"].year == dan.year and sve_karte[karta]["datum_prodaje"].month == dan.month and \
                sve_karte[karta]["datum_prodaje"].day == dan.day:
            broj += 1
            cena += svi_letovi[svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]
    return (broj, cena)


"""
Funkcija kao rezultat vraća dve vrednosti: broj karata čiji je dan polaska leta na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_polaska(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi: dict,
    dan: date
) -> tuple:
    broj = cena = 0
    for karta in sve_karte:
        if svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"].year == dan.year and svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"].month == dan.month and svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"].day == dan.day:
            broj += 1
            cena += svi_letovi[svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]
    return (broj, cena)


"""
Funkcija kao rezultat vraća dve vrednosti: broj karata koje je zadati prodavac prodao na zadati dan i njihovu 
ukupnu cenu. Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(
    sve_karte: dict,
    konkretni_letovi: dict,
    svi_letovi: dict,
    dan: date,
    prodavac: str
) -> tuple:
    broj = cena = 0
    for karta in sve_karte:
        if sve_karte[karta]["datum_prodaje"].year == dan.year and sve_karte[karta]["datum_prodaje"].month == dan.month and sve_karte[karta]["datum_prodaje"].day == dan.day and sve_karte[karta]["prodavac"] == prodavac:
            broj += 1
            cena += svi_letovi[konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["broj_leta"]]["cena"]
    return (broj, cena)


"""
Funkcija kao rezultat vraća rečnik koji za ključ ima dan prodaje, a za vrednost broj karata prodatih na taj dan.
Npr: {"2023-01-01": 20}
"""
def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi: dict
) -> dict: #ubc znaci ukupan broj i cena
    dan = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    ubc30 = {}
    for karta in sve_karte:
        if sve_karte[karta]["prodavac"] != 0:
            ubc30[sve_karte[karta]["prodavac"]] = (0, 0, sve_karte[karta]["prodavac"])
    for j in range(30):
        for karta in sve_karte:
            pom_datum = sve_karte[karta]["datum_prodaje"]
            if isinstance(sve_karte[karta]["datum_prodaje"], str):
                pom_datum = datetime.strptime(sve_karte[karta]["datum_prodaje"], "%d.%m.%Y.")
            if pom_datum.year == dan.year and pom_datum.month == dan.month and pom_datum.day == dan.day and sve_karte[karta]["prodavac"] != 0:
                ubc30[sve_karte[karta]["prodavac"]] = (ubc30[sve_karte[karta]["prodavac"]][0]+1,  ubc30[sve_karte[karta]["prodavac"]][1] + svi_letovi[svi_konkretni_letovi[sve_karte[karta]["sifra_konkretnog_leta"]]["broj_leta"]]["cena"], sve_karte[karta]["prodavac"])
        dan = dan - timedelta(days=1)

    return ubc30


