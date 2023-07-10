import common.konstante
from common import konstante
import csv

"""
Funkcija koja kreira novi rečnik koji predstavlja korisnika sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih korisnika proširenu novim korisnikom. Može se ponašati kao dodavanje ili ažuriranje, u zavisnosti od vrednosti
parametra azuriraj:
- azuriraj == False: kreira se novi korisnik. staro_korisnicko_ime ne mora biti prosleđeno.
Vraća grešku ako korisničko ime već postoji.
- azuriraj == True: ažurira se postojeći korisnik. Staro korisnicko ime mora biti prosleđeno. 
Vraća grešku ako korisničko ime ne postoji.

Ova funkcija proverava i validnost podataka o korisniku, koji su tipa string.

CHECKPOINT 1: Vraća string sa greškom ako podaci nisu validni.
    Hint: Postoji string funkcija koja proverava da li je string broj bez bacanja grešaka. Probajte da je pronađete.
ODBRANA: Baca grešku sa porukom ako podaci nisu validni.
"""
def kreiraj_korisnika(svi_korisnici: dict, azuriraj: bool, uloga: str, staro_korisnicko_ime: str, 
                      korisnicko_ime: str, lozinka: str, ime: str, prezime: str, email: str = "",
                      pasos: str = "", drzavljanstvo: str = "",
                      telefon: str = "", pol: str = "") -> dict:
    if isinstance(staro_korisnicko_ime, str) == False or isinstance(korisnicko_ime, str) == False or isinstance(lozinka, str) == False or isinstance(ime, str) == False or \
            isinstance(prezime, str) == False or isinstance(drzavljanstvo, str) == False or isinstance(pol, str) == False or isinstance(email, str) == False:
        raise Exception("Pogresan unos!")
    elif not pasos.isnumeric() or len(pasos) != 9:
        raise Exception("Pogresan unos pasosa!")
    elif not isinstance(telefon, str) or not telefon.isnumeric():
        raise Exception("Pogresan unos telefona!")
    elif uloga not in [konstante.ULOGA_KORISNIK, konstante.ULOGA_ADMIN, konstante.ULOGA_PRODAVAC]:
        raise Exception("Pogresan unos uloge!")
    if email.count("@") == 1:
        if email.split("@")[1].count(".") > 1:
            raise Exception("Pogresan unos emaila!")
    else:
        return "Email bez @"
    if not azuriraj and korisnicko_ime in svi_korisnici:
        raise Exception("Uneto korisnicko ime vec postoji!")
    if azuriraj and staro_korisnicko_ime not in svi_korisnici:
        raise Exception("Uneto korisnicko ime ne postoji!")
    if azuriraj and korisnicko_ime in svi_korisnici and korisnicko_ime != staro_korisnicko_ime:
        raise Exception("Uneto korisnicko ime je zauzeto!")
    if azuriraj == False:
        korisnik = {
            "uloga": uloga,
            "korisnicko_ime": korisnicko_ime,
            "lozinka": lozinka,
            "ime": ime,
            "prezime": prezime,
            "email": email,
            "pasos": pasos,
            "drzavljanstvo": drzavljanstvo,
            "telefon": telefon,
            "pol": pol
        }
        svi_korisnici[korisnicko_ime] = korisnik
    else:
        korisnik = {
            "uloga": konstante.ULOGA_KORISNIK,
            "korisnicko_ime": korisnicko_ime,
            "lozinka": lozinka,
            "ime": ime,
            "prezime": prezime,
            "email": email,
            "pasos": pasos,
            "drzavljanstvo": drzavljanstvo,
            "telefon": telefon,
            "pol": pol
        }
        svi_korisnici[staro_korisnicko_ime] = svi_korisnici[korisnicko_ime]
        svi_korisnici[korisnicko_ime] = korisnik

    return svi_korisnici

"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    with open(putanja, 'w', newline='') as file:
        polja = (
        "uloga", "korisnicko_ime", "lozinka", "ime", "prezime", "email", "pasos", "drzavljanstvo", "telefon", "pol")
        writer = csv.DictWriter(file, polja, delimiter=separator)
        for korisnik in svi_korisnici:
            writer.writerow(svi_korisnici[korisnik])
        file.close()


"""
Funkcija koja učitava sve korisnika iz fajla na putanji sa zadatim separatorom. Kao rezultat vraća učitane korisnike.
"""
def ucitaj_korisnike_iz_fajla(putanja: str, separator: str) -> dict:
    with open(putanja, 'r', newline='') as file:
        polja = ("uloga", "korisnicko_ime", "lozinka", "ime", "prezime", "email", "pasos", "drzavljanstvo", "telefon", "pol")
        reader = csv.DictReader(file, polja, delimiter=separator)
        korisnici = {}
        for row in reader:
            korisnici[row["korisnicko_ime"]] = row
    return korisnici


"""
Funkcija koja vraća korisnika sa zadatim korisničkim imenom i šifrom.
CHECKPOINT 1: Vraća string sa greškom ako korisnik nije pronađen.
ODBRANA: Baca grešku sa porukom ako korisnik nije pronađen.
"""
def login(svi_korisnici, korisnicko_ime, lozinka) -> dict:
    if korisnicko_ime not in svi_korisnici:
        raise Exception("Uneto korisnicko ime ne postoji!")
    elif lozinka == svi_korisnici[korisnicko_ime]["lozinka"]:
        return svi_korisnici[korisnicko_ime]
    else:
        raise Exception("Pogresna lozinka!")

"""
Funkcija koja vrsi log out
*
"""
def logout(korisnicko_ime: str):
    korisnik = {
        "uloga": 0
    }
    return korisnik
