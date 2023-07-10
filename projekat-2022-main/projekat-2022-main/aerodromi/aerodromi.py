import csv

"""
Funkcija kreira rečnik za novi aerodrom i dodaje ga u rečnik svih aerodroma.
Kao rezultat vraća rečnik svih aerodroma sa novim aerodromom.
"""
def kreiranje_aerodroma(
    svi_aerodromi: dict,
    skracenica: str ="",
    pun_naziv: str ="",
    grad: str ="",
    drzava: str =""
) -> dict:
    if not isinstance(skracenica, str) or len(skracenica) != 3:
        raise Exception("Prazna skracenica!")
    if not isinstance(pun_naziv, str) or len(pun_naziv) != 7:
        raise Exception("Pogresan pun naziv!")
    if not isinstance(grad, str) or len(grad) != 7:
        raise Exception("Pogresan grad!")
    if not isinstance(drzava, str) or len(drzava) != 7:
        raise Exception("Pogresna drzava!")
    aerodrom = {
        "skracenica": skracenica,
        "pun_naziv": pun_naziv,
        "grad": grad,
        "drzava": drzava
    }
    svi_aerodromi[skracenica] = aerodrom
    return svi_aerodromi

"""
Funkcija koja čuva aerodrome u fajl.
"""
def sacuvaj_aerodrome(putanja: str, separator: str, svi_aerodromi: dict):
    with open(putanja, 'w', newline='') as file:
        polja = ("skracenica", "pun_naziv", "grad", "drzava")
        writer = csv.DictWriter(file, polja, delimiter=separator)
        for aerodrom in svi_aerodromi:
            writer.writerow(svi_aerodromi[aerodrom])
        file.close()

"""
Funkcija koja učitava aerodrome iz fajla.
"""
def ucitaj_aerodrom(putanja: str, separator: str) -> dict:
    with open(putanja, 'r', newline='') as file:
        polja = ("skracenica", "pun_naziv", "grad", "drzava")
        reader = csv.DictReader(file, polja, delimiter=separator)
        aerodromi = {}
        for row in reader:
            aerodromi[row["skracenica"]] = row
    return aerodromi