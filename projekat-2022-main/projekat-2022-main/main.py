#autor: Nikola Bandulaja SV74/2022
#projekat je zipovan 1.14.2023. u 21:58 i sadrzi poslednju verziju testova, sa ispravljenom greskom u pozivu funkcije
#pregled nerealizovanih letova, kao i u testu za konkretne letove
import copy
from datetime import datetime, timedelta, time

from common import konstante
from izvestaji import izvestaji
from karte import karte
from konkretni_letovi import konkretni_letovi
from korisnici import korisnici
from letovi import letovi
from model import model
from model_aviona import model_aviona
from collections import OrderedDict
from operator import getitem

def meni_neregistrovani():
    print("\n1. Prijava na sistem")
    print("\n2. Izlaz iz aplikacije")
    print("\n3. Pregled nerealizovanih letova")
    print("\n4. Pretraga letova")
    print("\n5. Prikaz 10 najjeftinijih letova izmedju zadatog polazista i odredista")
    print("\n6. Fleksibilni polasci")
    print("\n7. Registracija na sistem")

def meni_kupac():
    print("\n1. Izlaz iz aplikacije")
    print("\n2. Pregled nerealizovanih letova")
    print("\n3. Pretraga letova")
    print("\n4. Prikaz 10 najjeftinijih letova izmedju zadatog polazista i odredista")
    print("\n5. Fleksibilni polasci")
    print("\n6. Odjava sa sistema")
    print("\n7. Kupovina karata")
    print("\n8. Pregled nerealizovanih karata")
    print("\n9. Prijava na let(check-in)")

def meni_prodavac():
    print("\n1. Izlaz iz aplikacije")
    print("\n2. Pregled nerealizovanih letova")
    print("\n3. Pretraga letova")
    print("\n4. Prikaz 10 najjeftinijih letova izmedju zadatog polazista i odredista")
    print("\n5. Fleksibilni polasci")
    print("\n6. Odjava sa sistema")
    print("\n7. Prodaja karata")
    print("\n8. Prijava na let(check-in)")
    print("\n9. Izmena karte")
    print("\n10. Brisanje karte")
    print("\n11. Pretraga prodatih karata")

def meni_menadzer():
    print("\n1. Izlaz iz aplikacije")
    print("\n2. Pretraga nerealizovanih letova")
    print("\n3. Pretraga letova")
    print("\n4. Prikaz 10 najjeftinijih letova izmedju zadatog polazista i odredista")
    print("\n5. Fleksibilni polasci")
    print("\n6. Odjava sa sistema")
    print("\n7. Pretraga prodatih karata")
    print("\n8. Registracija novih prodavaca")
    print("\n9. Kreiranje letova")
    print("\n10. Izmena letova")
    print("\n11. Brisanje karata")
    print("\n12. Izvestavanje")
    print("\n13. Dodatna pretraga letova po polazistu, odredistu i datumu polaska")


def tabela_letova(letovi):
    print(f"{'BROJ LETA':^15}{'||'}{'POLAZISTE':^15}{'||'}{'ODREDISTE':^15}{'||'}{'PREVOZNIK':^20}{'||'}{'VREME POLETANJA':^20}{'||'}{'VREME SLETANJA':^20}{'||'}{'DATUM POCETKA OPERATIVNOSTI':^30}{'||'}{'DATUM KRAJA OPERATIVNOSTI':^30}{'||'}{'CENA':^13}")
    print("="*191)
    for let in letovi:
        print(f"{letovi[let]['broj_leta']:^15}{'||'}{letovi[let]['sifra_polazisnog_aerodroma']:^15}{'||'}{letovi[let]['sifra_odredisnog_aerodorma']:^15}{'||'}{letovi[let]['prevoznik']:^20}{'||'}{letovi[let]['vreme_poletanja']:^20}{'||'}{letovi[let]['vreme_sletanja']:^20}{'||'}{letovi[let]['datum_pocetka_operativnosti'].strftime('%Y-%m-%d %H:%M:%S'):^30}{'||'}{letovi[let]['datum_kraja_operativnosti'].strftime('%Y-%m-%d %H:%M:%S'):^30}{'||'}{letovi[let]['cena']:^13}")

def tabela_konkretnih_letova(letovi):
    print(f"{'SIFRA KONKRETNOG LETA':^25}{'||'}{'BROJ LETA':^15}{'||'}{'DATUM I VREME POLASKA':^30}{'||'}{'DATUM I VREME DOLASKA':^30}")
    print("="*102)
    for let in letovi:
        print(f"{letovi[let]['sifra']:^25}{'||'}{letovi[let]['broj_leta']:^15}{'||'}{letovi[let]['datum_i_vreme_polaska'].strftime('%Y-%m-%d %H:%M:%S'):^30}{'||'}{letovi[let]['datum_i_vreme_dolaska'].strftime('%Y-%m-%d %H:%M:%S'):^30}")

def konvertuj_konkretne_u_dict(letovi):
    returnDict = {}
    for i in range(len(letovi)):
        returnDict[letovi[i]["sifra"]] = letovi[i]
    return returnDict

def konvertuj_u_dict(letovi):
    returnDict = {}
    for i in range(len(letovi)):
        returnDict[letovi[i]["broj_leta"]] = letovi[i]
    return returnDict

def tabela_karte(karte):
    print(f"{'BROJ KARTE':^15}{'||'}{'SIFRA KONKRETNOG LETA':^25}{'||'}{'KUPAC':^30}{'||'}{'STATUS':^35}")
    print("=" * 105)
    for karta in karte:
        print(f"{karte[karta]['broj_karte']:^15}{'||'}{karte[karta]['sifra_konkretnog_leta']:^25}{'||'}{karte[karta]['kupac']['korisnicko_ime']:^30}{'||'}{karte[karta]['status']:^35}")

def karte_u_dict(karte):
    returnDict = {}
    for i in range(len(karte)):
        returnDict[karte[i]["broj_karte"]] = karte[i]
    return  returnDict

def azuriraj_pom_karte(sve_karte):
    pom_karte = copy.deepcopy(sve_karte)
    for karta in pom_karte:
        if pom_karte[karta]["prodavac"] != 0:
            pom_karte[karta]["prodavac"] = pom_karte[karta]["prodavac"]["korisnicko_ime"]
        pom_karte[karta]["datum_prodaje"] = datetime.strptime(pom_karte[karta]["datum_prodaje"], "%Y-%m-%d %H:%M:%S.%f")
    return pom_karte

kraj = False
korisnik = {"uloga": 0}
uloga = korisnik["uloga"]
izbor = 0

svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla("korisnici.csv", "|")
sve_karte = karte.ucitaj_karte_iz_fajla("karte.csv", "|")
svi_letovi = letovi.ucitaj_letove_iz_fajla("letovi.csv", "|")
svi_konkretni_letovi = konkretni_letovi.ucitaj_konkretan_let("konkretni_letovi.csv", "|")
svi_modeli = model_aviona.ucitaj_modele_aviona("modeli.csv", "|")

pom_karte = azuriraj_pom_karte(sve_karte)

while not kraj:

    match uloga:
        case 0:
            meni_neregistrovani()
        case konstante.ULOGA_KORISNIK:
            meni_kupac()
        case konstante.ULOGA_PRODAVAC:
            meni_prodavac()
        case konstante.ULOGA_ADMIN:
            meni_menadzer()

    while True:
        try:
            print("\nIzaberite neku od opcija: ")
            izbor = int(input())
            if uloga == 0 and (izbor < 1 or izbor > 8):
                print("Pogresan unos opcije")
                continue
            if uloga ==  konstante.ULOGA_KORISNIK and (izbor < 1 or izbor > 10):
                print("Pogresan unos opcije")
                continue
            if uloga == konstante.ULOGA_PRODAVAC and (izbor < 1 or izbor > 12):
                print("Pogresan unos opcije")
                continue
            if uloga == konstante.ULOGA_ADMIN and (izbor < 1 or izbor > 14):
                print("Pogresan unos opcije")
                continue
            break
        except:
            print("Pogresan unos opcije")
            continue

    match uloga:
        case 0:
            match izbor:
                case 1:
                    try:
                        print("Unesite korisnicko ime: ")
                        login_korisnicko_ime = input()
                        print("Unesite lozinku: ")
                        login_lozinka = input()
                        korisnik = korisnici.login(svi_korisnici, login_korisnicko_ime, login_lozinka)
                        uloga = korisnik["uloga"]
                    except:
                        print("Greska pri logovanju!")
                        continue
                case 2:
                    kraj = True
                    print("Kraj rada programa!")
                    break
                case 3:
                    try:
                        nerealizovani_letovi = letovi.pregled_nerealizovanih_letova(svi_letovi)
                        tabela_letova(konvertuj_u_dict(nerealizovani_letovi))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 4:
                    try:
                        print("Unesite polaziste: ")
                        polaziste = input()
                        print("Unesite odrediste: ")
                        odrediste = input()
                        print("Unesite datum polaska: ")
                        datum_polaska = input()
                        if datum_polaska != "":
                            datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d")
                        else:
                            datum_polaska = None
                        print("Unesite datum dolaska: ")
                        datum_dolaska = input()
                        if datum_dolaska != "":
                            datum_dolaska = datetime.strptime(datum_dolaska, "%Y-%m-%d")
                        else:
                            datum_dolaska = None
                        print("Unesite vreme poletanja: ")
                        vreme_poletanja = input()
                        print("Unesite vreme sletanja: ")
                        vreme_sletanja = input()
                        print("Unesite prevoznika: ")
                        prevoznik = input()
                        rezultat_pretrage = letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste,
                                                                   odrediste, datum_polaska, datum_dolaska,
                                                                   vreme_poletanja, vreme_sletanja, prevoznik)
                        tabela_konkretnih_letova(konvertuj_konkretne_u_dict(rezultat_pretrage))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 5:
                    try:
                        print("Unesite polaziste: ")
                        polaziste = input()
                        print("Unesite odrediste: ")
                        odrediste = input()
                        top10 = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, polaziste, odrediste)
                        tabela_letova(konvertuj_u_dict(top10))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 6:
                    try:
                        print("Polaziste: ")
                        polaziste = input()
                        print("Odrediste: ")
                        odrediste = input()
                        print("Broj fleksibilnih dana: ")
                        br_dana = input()
                        print("Datum polaska: ")
                        datum_polaska = input()
                        datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d")
                        fleksibilni = letovi.fleksibilni_polasci(svi_letovi, svi_konkretni_letovi, polaziste, odrediste,
                                                                 datum_polaska, int(br_dana), None)
                        tabela_konkretnih_letova(konvertuj_konkretne_u_dict(fleksibilni))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 7:
                    try:
                        print("Korisnicko ime: ")
                        korisnicko_ime = input()
                        print("Lozinka: ")
                        lozinka = input()
                        print("Ime: ")
                        ime = input()
                        print("Prezime: ")
                        prezime = input()
                        print("Email: ")
                        email = input()
                        print("Pasos: ")
                        pasos = input()
                        print("Drzavljanstvo: ")
                        drzavljanstvo = input()
                        print("Telefon: ")
                        telefon = input()
                        print("Pol: ")
                        pol = input()
                        svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_KORISNIK, "",
                                                                    korisnicko_ime, lozinka, ime, prezime, email, pasos,
                                                                    drzavljanstvo, telefon, pol)
                        korisnici.sacuvaj_korisnike("korisnici.csv", "|", svi_korisnici)
                        print("Uspesno ste se registrovali!")
                    except:
                        print("Doslo je do greske!")
                        continue
        case konstante.ULOGA_KORISNIK:
            match izbor:
                case 1:
                    kraj = True
                    print("Kraj rada programa!")
                    break
                case 2:
                    try:
                        nerealizovani_letovi = letovi.pregled_nerealizovanih_letova(svi_letovi)
                        tabela_letova(konvertuj_u_dict(nerealizovani_letovi))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 3:
                    try:
                        print("Unesite polaziste: ")
                        polaziste = input()
                        print("Unesite odrediste: ")
                        odrediste = input()
                        print("Unesite datum polaska: ")
                        datum_polaska = input()
                        if datum_polaska != "":
                            datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d")
                        else:
                            datum_polaska = None
                        print("Unesite datum dolaska: ")
                        datum_dolaska = input()
                        if datum_dolaska != "":
                            datum_dolaska = datetime.strptime(datum_dolaska, "%Y-%m-%d")
                        else:
                            datum_dolaska = None
                        print("Unesite vreme poletanja: ")
                        vreme_poletanja = input()
                        print("Unesite vreme sletanja: ")
                        vreme_sletanja = input()
                        print("Unesite prevoznika: ")
                        prevoznik = input()
                        rezultat_pretrage = letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste,
                                                                   odrediste, datum_polaska, datum_dolaska,
                                                                   vreme_poletanja, vreme_sletanja, prevoznik)
                        rezultat_pretrage = letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste,
                                                                   odrediste, datum_polaska, datum_dolaska,
                                                                   vreme_poletanja, vreme_sletanja, prevoznik)
                        tabela_konkretnih_letova(konvertuj_konkretne_u_dict(rezultat_pretrage))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 4:
                    try:
                        print("Unesite polaziste: ")
                        polaziste = input()
                        print("Unesite odrediste: ")
                        odrediste = input()
                        top10 = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, polaziste, odrediste)
                        top10 = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, polaziste, odrediste)
                        tabela_letova(konvertuj_u_dict(top10))
                    except:
                        print("Doslo je do greske")
                        continue
                case 5:
                    try:
                        print("Polaziste: ")
                        polaziste = input()
                        print("Odrediste: ")
                        odrediste = input()
                        print("Broj fleksibilnih dana: ")
                        br_dana = input()
                        print("Datum polaska: ")
                        datum_polaska = input()
                        datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d")
                        fleksibilni = letovi.fleksibilni_polasci(svi_letovi, svi_konkretni_letovi, polaziste, odrediste,
                                                                 datum_polaska, int(br_dana), None)
                        tabela_konkretnih_letova(konvertuj_konkretne_u_dict(fleksibilni))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 6:
                    korisnik = korisnici.logout(korisnik["korisnicko_ime"])
                    uloga = korisnik["uloga"]
                case 7:
                    try:
                        while True:
                            print("Sifra konkretnog leta: ")
                            sifra_konkretnog_leta = eval(input())
                            zauzetost = svi_konkretni_letovi[sifra_konkretnog_leta]["zauzetost"]
                            ind = 0
                            for x in zauzetost:
                                for j in x:
                                    if x[j] == True:
                                        continue
                                    else:
                                        ind = 1
                                        break
                            if ind == 0:
                                print("Nema mesta!")
                                raise Exception("Nema mesta!")
                            ind = True
                            while ind:
                                print("Da li kupujete kartu za sebe(da/ne): ")
                                nastavak = input()
                                if nastavak == "da" or nastavak == "ne":
                                    ind = False
                            putnici = []
                            if nastavak == "da":
                                putnici.append(korisnik)
                                tapl = karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra_konkretnog_leta,
                                                            putnici,
                                                            svi_konkretni_letovi[sifra_konkretnog_leta]["zauzetost"],
                                                            korisnik, prodavac=None)
                                sve_karte = tapl[1]
                                karte.sacuvaj_karte(sve_karte, "karte.csv", "|")
                                sve_karte = karte.ucitaj_karte_iz_fajla("karte.csv", "|")
                                pom_karte = azuriraj_pom_karte(sve_karte)
                                print("Karta je uspesno kupljena!")
                            else:
                                print("Unesite korisnicko ime korisnika za kojeg kupujete kartu: ")
                                saputnik_korisnicko_ime = input()
                                if saputnik_korisnicko_ime not in svi_korisnici:
                                    print("Ime neregistrovanog saputnika: ")
                                    ime_saputnika = input()
                                    print("Prezime neregistrovanog saputnika: ")
                                    prezime_saputnika = input()
                                    print("Drzavljanstvo saputnika: ")
                                    drzavljanstvo_saputnika = input()
                                    print("Broj pasosa saputnika: ")
                                    pasos_saputnika = input()
                                    print("Telefon saputnika: ")
                                    telefon_saputnika = input()
                                    putnici.append({"korisnicko_ime": saputnik_korisnicko_ime,
                                                    "ime": ime_saputnika,
                                                    "prezime": prezime_saputnika,
                                                    "uloga": konstante.ULOGA_KORISNIK,
                                                    "drzavljanstvo": drzavljanstvo_saputnika,
                                                    "pasos": pasos_saputnika,
                                                    "telefon": telefon_saputnika
                                    })
                                else:
                                    putnici.append(svi_korisnici[saputnik_korisnicko_ime])
                                tapl = karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra_konkretnog_leta,
                                                        putnici,
                                                        svi_konkretni_letovi[sifra_konkretnog_leta]["zauzetost"],
                                                        korisnik, prodavac=None)
                                sve_karte = tapl[1]
                                karte.sacuvaj_karte(sve_karte, "karte.csv", "|")
                                sve_karte = karte.ucitaj_karte_iz_fajla("karte.csv", "|")
                                pom_karte = azuriraj_pom_karte(sve_karte)
                                print("Karta je uspesno kupljena!")
                            ind = True
                            while ind:
                                print("Da li zelite da nastavite sa kupovinom(da/ne): ")
                                nastavak = input()
                                if nastavak == "da" or nastavak == "ne":
                                    ind = False
                            if nastavak == "da":
                                ind_povezani = True
                                continue
                            else:
                                break
                    except:
                        print("Doslo je do greske!")
                        continue
                case 8:
                        karte_lista = []
                        for karta in sve_karte:
                            karte_lista.append(sve_karte[karta])
                        nerealizovane_karte = karte.pregled_nerealizovanaih_karata(korisnik, karte_lista)
                        tabela_karte(karte_u_dict(nerealizovane_karte))

                case 9:
                    try:
                        print("Unesite broj karte: ")
                        broj_karte = eval(input())
                        karta = sve_karte[broj_karte]
                        konkretan_let = svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]
                        zauzetost = konkretan_let["zauzetost"]
                        svaki_let = svi_letovi[konkretan_let["broj_leta"]]
                        model = svaki_let["model"]
                        br_redova = model["broj_redova"]
                        slova = model["pozicije_sedista"]
                        kolone = len(model["pozicije_sedista"])
                        for i in range(br_redova):
                            print("Red", i+1)
                            for j in range(kolone):
                                if zauzetost[i][j] == True:
                                    print("X")
                                else:
                                    print(slova[j])
                        print("Unesite red: ")
                        red = eval(input())
                        print("Unesite poziciju: ")
                        pozicija = input()
                        tapl = letovi.checkin(karta, svi_letovi, konkretan_let, red, pozicija)
                        svi_konkretni_letovi[karta["sifra_konkretnog_leta"]] = tapl[0]
                        sve_karte[broj_karte] = tapl[1]
                        konkretni_letovi.sacuvaj_kokretan_let("konkretni_letovi.csv", "|", svi_konkretni_letovi)
                        karte.sacuvaj_karte(sve_karte, "karte.csv", "|")
                        print("Uspesno ste se prijavili na let!")
                    except:
                        print("Doslo je do greske!")
                        continue
        case konstante.ULOGA_PRODAVAC:
            match izbor:
                case 1:
                    kraj = True
                    print("Kraj rada programa!")
                    break
                case 2:
                    try:
                        nerealizovani_letovi = letovi.pregled_nerealizovanih_letova(svi_letovi)
                        tabela_letova(konvertuj_u_dict(nerealizovani_letovi))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 3:
                    try:
                        print("Unesite polaziste: ")
                        polaziste = input()
                        print("Unesite odrediste: ")
                        odrediste = input()
                        print("Unesite datum polaska: ")
                        datum_polaska = input()
                        if datum_polaska != "":
                            datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d")
                        else:
                            datum_polaska = None
                        print("Unesite datum dolaska: ")
                        datum_dolaska = input()
                        if datum_dolaska != "":
                            datum_dolaska = datetime.strptime(datum_dolaska, "%Y-%m-%d")
                        else:
                            datum_dolaska = None
                        print("Unesite vreme poletanja: ")
                        vreme_poletanja = input()
                        print("Unesite vreme sletanja: ")
                        vreme_sletanja = input()
                        print("Unesite prevoznika: ")
                        prevoznik = input()
                        rezultat_pretrage = letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste,
                                                                   odrediste, datum_polaska, datum_dolaska,
                                                                   vreme_poletanja, vreme_sletanja, prevoznik)
                        rezultat_pretrage = letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste,
                                                                   odrediste, datum_polaska, datum_dolaska,
                                                                   vreme_poletanja, vreme_sletanja, prevoznik)
                        tabela_konkretnih_letova(konvertuj_konkretne_u_dict(rezultat_pretrage))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 4:
                    try:
                        print("Unesite polaziste: ")
                        polaziste = input()
                        print("Unesite odrediste: ")
                        odrediste = input()
                        top10 = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, polaziste, odrediste)
                        top10 = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, polaziste, odrediste)
                        tabela_letova(konvertuj_u_dict(top10))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 5:
                    try:
                        print("Polaziste: ")
                        polaziste = input()
                        print("Odrediste: ")
                        odrediste = input()
                        print("Broj fleksibilnih dana: ")
                        br_dana = input()
                        print("Datum polaska: ")
                        datum_polaska = input()
                        datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d")
                        fleksibilni = letovi.fleksibilni_polasci(svi_letovi, svi_konkretni_letovi, polaziste, odrediste,
                                                                 datum_polaska, int(br_dana), None)
                        tabela_konkretnih_letova(konvertuj_konkretne_u_dict(fleksibilni))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 6:
                    korisnik = korisnici.logout(korisnik["korisnicko_ime"])
                    uloga = korisnik["uloga"]
                case 7:
                    try:
                        while True:
                            print("Sifra konkretnog leta: ")
                            sifra_konkretnog_leta = eval(input())
                            zauzetost = svi_konkretni_letovi[sifra_konkretnog_leta]["zauzetost"]
                            for x in zauzetost:
                                for j in x:
                                    if x[j] == True:
                                        continue
                                    else:
                                        ind = 1
                                        break
                            if ind == 0:
                                print("Nema mesta!")
                                raise Exception("Nema mesta!")
                            print("Korisnicko ime kupca: ")
                            korisnicko_ime_kupca = input()
                            if korisnicko_ime_kupca not in svi_korisnici:
                                print("Ime neregistrovanog kupca: ")
                                ime_kupca = input()
                                print("Prezime neregistrovanog kupca: ")
                                prezime_kupca = input()
                                print("Telefon: ")
                                telefon = input()
                                print("Email: ")
                                email = input()
                                print("Drzavljanstvo: ")
                                drzavljanstvo = input()
                                print("Broj pasosa: ")
                                pasos = input()
                                kupac = {"korisnicko_ime": korisnicko_ime_kupca,
                                         "ime": ime_kupca,
                                         "prezime": prezime_kupca,
                                         "uloga": konstante.ULOGA_KORISNIK,
                                         "telefon": telefon,
                                         "email": email,
                                         "drzavljanstvo": drzavljanstvo,
                                         "pasos": pasos}
                            else:
                                kupac = svi_korisnici[korisnicko_ime_kupca]
                            tapl = karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra_konkretnog_leta,
                                                        [kupac],
                                                        svi_konkretni_letovi[sifra_konkretnog_leta]["zauzetost"],
                                                        kupac, prodavac=korisnik)
                            sve_karte = tapl[1]
                            karte.sacuvaj_karte(sve_karte, "karte.csv", "|")
                            sve_karte = karte.ucitaj_karte_iz_fajla("karte.csv", "|")
                            pom_karte = azuriraj_pom_karte(sve_karte)
                            print("Karta je uspesno prodata!")
                            ind = True
                            while ind:
                                print("Da li zelite da nastavite sa kupovinom(da/ne): ")
                                nastavak = input()
                                if nastavak == "da" or nastavak == "ne":
                                    ind = False
                            if nastavak == "da":
                                continue
                            else:
                                break
                    except:
                        print("Doslo je do greske!")
                        continue
                case 8:
                    try:
                        print("Unesite broj karte: ")
                        broj_karte = eval(input())
                        karta = sve_karte[broj_karte]
                        konkretan_let = svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]
                        zauzetost = konkretan_let["zauzetost"]
                        svaki_let = svi_letovi[konkretan_let["broj_leta"]]
                        model = svaki_let["model"]
                        br_redova = model["broj_redova"]
                        slova = model["pozicije_sedista"]
                        kolone = len(model["pozicije_sedista"])
                        for i in range(br_redova):
                            print("Red", i+1)
                            for j in range(kolone):
                                if zauzetost[i][j] == True:
                                    print("X")
                                else:
                                    print(slova[j])
                        print("Unesite red: ")
                        red = eval(input())
                        print("Unesite poziciju: ")
                        pozicija = input()
                        tapl = letovi.checkin(karta, svi_letovi, konkretan_let, red, pozicija)
                        svi_konkretni_letovi[karta["sifra_konkretnog_leta"]] = tapl[0]
                        sve_karte[broj_karte] = tapl[1]
                        konkretni_letovi.sacuvaj_kokretan_let("konkretni_letovi.csv", "|", svi_konkretni_letovi)
                        karte.sacuvaj_karte(sve_karte, "karte.csv", "|")
                        pom_karte = azuriraj_pom_karte(sve_karte)
                        print("Uspesno ste prijavili korisnika na let!")
                    except:
                        print("Doslo je do greske!")
                        continue
                case 9:
                    try:
                        print("Broj karte za izmenu: ")
                        broj_karte = eval(input())
                        if broj_karte not in sve_karte:
                            print("Nepostojeci broj karte!")
                            raise Exception("Karta sa tim brojem ne postoji!")
                        print("Nova sifra konkretnog leta: ")
                        nova_sifra = eval(input())
                        konkretan_let = svi_konkretni_letovi[sve_karte[broj_karte]["sifra_konkretnog_leta"]]
                        zauzetost = konkretan_let["zauzetost"]
                        svaki_let = svi_letovi[konkretan_let["broj_leta"]]
                        model = svaki_let["model"]
                        br_redova = model["broj_redova"]
                        slova = model["pozicije_sedista"]
                        kolone = len(model["pozicije_sedista"])
                        print("Red novog sedista: ")
                        red = eval(input())
                        if red < 1 or red > br_redova:
                            raise Exception("Pogresan red!")
                        print("Pozicija novog sedista: ")
                        pozicija = input()
                        novo_sediste = pozicija + str(red)
                        pozicija = ord(pozicija) - 65
                        if pozicija < 0:
                            raise Exception("Pogresna pozicija!")
                        if zauzetost[red - 1][pozicija] == True:
                            raise Exception("Mesto je zauzeto!")
                        sve_karte = karte.izmena_karte(sve_karte, svi_konkretni_letovi, broj_karte, nova_sifra, None, novo_sediste)
                        karte.sacuvaj_karte(sve_karte, "karte.csv", "|")
                        print("Uspesno ste izmenili kartu!")
                    except:
                        print("Doslo je do greske!")
                        continue
                case 10:
                    try:
                        print("Unesite broj karte za brisanje: ")
                        broj_karte = eval(input())
                        sve_karte = karte.brisanje_karte(korisnik, sve_karte, broj_karte)
                        karte.sacuvaj_karte(sve_karte, "karte.csv", "|")
                        print("Karta je uspesno oznacena za brisanje!")
                    except:
                        print("Doslo je do greske!")
                        continue
                case 11:
                    try:
                        print("Polaziste: ")
                        polaziste = input()
                        print("Odrediste: ")
                        odrediste = input()
                        print("Datum polaska: ")
                        datum_polaska = input()
                        if datum_polaska != "":
                            datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d")
                        else:
                            datum_polaska = None
                        print("Datum dolaska: ")
                        datum_dolaska = input()
                        if datum_dolaska != "":
                            datum_dolaska = datetime.strptime(datum_dolaska, "%Y-%m-%d")
                        else:
                            datum_dolaska = None
                        print("Korisnicko ime putnika: ")
                        korisnicko_ime_putnika = input()
                        if korisnicko_ime_putnika == "":
                            korisnicko_ime_putnika = None
                        prodate_karte = karte.pretraga_prodatih_karata(sve_karte, svi_letovi, svi_konkretni_letovi,
                                                                       polaziste, odrediste, datum_polaska,
                                                                       datum_dolaska, korisnicko_ime_putnika)
                        tabela_karte(karte_u_dict(prodate_karte))
                    except:
                        print("Doslo je do greske!")
                        continue

        case konstante.ULOGA_ADMIN:
            match izbor:
                case 1:
                    kraj = True
                    print("Kraj rada programa!")
                    break
                case 2:
                    try:
                        nerealizovani_letovi = letovi.pregled_nerealizovanih_letova(svi_letovi)
                        tabela_letova(konvertuj_u_dict(nerealizovani_letovi))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 3:
                    try:
                        print("Unesite polaziste: ")
                        polaziste = input()
                        print("Unesite odrediste: ")
                        odrediste = input()
                        print("Unesite datum polaska: ")
                        datum_polaska = input()
                        if datum_polaska != "":
                            datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d")
                        else:
                            datum_polaska = None
                        print("Unesite datum dolaska: ")
                        datum_dolaska = input()
                        if datum_dolaska != "":
                            datum_dolaska = datetime.strptime(datum_dolaska, "%Y-%m-%d")
                        else:
                            datum_dolaska = None
                        print("Unesite vreme poletanja: ")
                        vreme_poletanja = input()
                        print("Unesite vreme sletanja: ")
                        vreme_sletanja = input()
                        print("Unesite prevoznika: ")
                        prevoznik = input()
                        rezultat_pretrage = letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste,
                                                                   odrediste, datum_polaska, datum_dolaska,
                                                                   vreme_poletanja, vreme_sletanja, prevoznik)
                        rezultat_pretrage = letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste,
                                                                   odrediste, datum_polaska, datum_dolaska,
                                                                   vreme_poletanja, vreme_sletanja, prevoznik)
                        tabela_konkretnih_letova(konvertuj_konkretne_u_dict(rezultat_pretrage))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 4:
                    try:
                        print("Unesite polaziste: ")
                        polaziste = input()
                        print("Unesite odrediste: ")
                        odrediste = input()
                        top10 = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, polaziste, odrediste)
                        top10 = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, polaziste, odrediste)
                        tabela_letova(konvertuj_u_dict(top10))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 5:
                    try:
                        print("Polaziste: ")
                        polaziste = input()
                        print("Odrediste: ")
                        odrediste = input()
                        print("Broj fleksibilnih dana: ")
                        br_dana = input()
                        print("Datum polaska: ")
                        datum_polaska = input()
                        datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d")
                        fleksibilni = letovi.fleksibilni_polasci(svi_letovi, svi_konkretni_letovi, polaziste, odrediste,
                                                                 datum_polaska, int(br_dana), None)
                        tabela_konkretnih_letova(konvertuj_konkretne_u_dict(fleksibilni))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 6:
                    korisnik = korisnici.logout(korisnik["korisnicko_ime"])
                    uloga = korisnik["uloga"]
                case 7:
                    try:
                        print("Polaziste: ")
                        polaziste = input()
                        print("Odrediste: ")
                        odrediste = input()
                        print("Datum polaska: ")
                        datum_polaska = input()
                        if datum_polaska != "":
                            datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d")
                        else:
                            datum_polaska = None
                        print("Datum dolaska: ")
                        datum_dolaska = input()
                        if datum_dolaska != "":
                            datum_dolaska = datetime.strptime(datum_dolaska, "%Y-%m-%d")
                        else:
                            datum_dolaska = None
                        print("Korisnicko ime putnika: ")
                        korisnicko_ime_putnika = input()
                        if korisnicko_ime_putnika == "":
                            korisnicko_ime_putnika = None
                        prodate_karte = karte.pretraga_prodatih_karata(sve_karte, svi_letovi, svi_konkretni_letovi,
                                                                       polaziste, odrediste, datum_polaska,
                                                                       datum_dolaska, korisnicko_ime_putnika)
                        tabela_karte(karte_u_dict(prodate_karte))
                    except:
                        print("Doslo je do greske!")
                        continue
                case 8:
                    try:
                        print("Korisnicko ime: ")
                        korisnicko_ime = input()
                        print("Lozinka: ")
                        lozinka = input()
                        print("Ime: ")
                        ime = input()
                        print("Prezime: ")
                        prezime = input()
                        print("Email: ")
                        email = input()
                        print("Pasos: ")
                        pasos = input()
                        print("Drzavljanstvo: ")
                        drzavljanstvo = input()
                        print("Telefon: ")
                        telefon = input()
                        print("Pol: ")
                        pol = input()
                        svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_PRODAVAC, "",
                                                                    korisnicko_ime, lozinka, ime, prezime, email, pasos,
                                                                    drzavljanstvo, telefon, pol)
                        korisnici.sacuvaj_korisnike("korisnici.csv", "|", svi_korisnici)
                        print("Uspesno ste registrovali prodavca!")
                    except:
                        print("Doslo je do greske!")
                        continue
                case 9:
                    try:
                        print("Broj leta: ")
                        broj_leta = input()
                        print("Polaziste: ")
                        polaziste = input()
                        print("Odrediste: ")
                        odrediste = input()
                        print("Vreme poletanja: ")
                        vreme_poletanja = input()
                        print("Vreme sletanja: ")
                        vreme_sletanja = input()
                        print("Sletanje sutra: ")
                        sletanje_sutra = input()
                        if sletanje_sutra == "False":
                            sletanje_sutra = False
                        elif sletanje_sutra == "True":
                            sletanje_sutra = True
                        print("Prevoznik: ")
                        prevoznik = input()
                        print("Dani(u formatu 1,2,3,4,...): ")
                        dani = input()
                        dani = dani.split(',')
                        for i in range(len(dani)):
                            dani[i] = int(dani[i])
                        print("Sifra modela: ")
                        sifra_modela = eval(input())
                        model = svi_modeli[sifra_modela]
                        print("Cena: ")
                        cena = input()
                        cena = float(cena)
                        print("Datum pocetka operativnosti: ")
                        datum_pocetka = input()
                        datum_pocetka = datetime.strptime(datum_pocetka, "%Y-%m-%d")
                        print("Datum kraja operativnosti: ")
                        datum_kraja = input()
                        datum_kraja = datetime.strptime(datum_kraja, "%Y-%m-%d")
                        svi_letovi = letovi.kreiranje_letova(svi_letovi, broj_leta, polaziste, odrediste,
                                                             vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik,
                                                             dani, model, cena, datum_pocetka, datum_kraja)
                        svi_konkretni_letovi = konkretni_letovi.kreiranje_konkretnog_leta(svi_konkretni_letovi, svi_letovi[broj_leta])
                        for let in svi_konkretni_letovi:
                            if svi_konkretni_letovi[let]["broj_leta"] == broj_leta:
                                svi_konkretni_letovi[let]["zauzetost"] = letovi.podesi_matricu_zauzetosti(svi_letovi,svi_konkretni_letovi[let])
                        letovi.sacuvaj_letove("letovi.csv", "|", svi_letovi)
                        konkretni_letovi.sacuvaj_kokretan_let("konkretni_letovi.csv", "|", svi_konkretni_letovi)
                        print("Let i njegovi konkretni letovi su uspesno kreirani!")
                    except:
                        print("Doslo je do greske!")
                        continue
                case 10:
                    try:
                        print("Broj leta: ")
                        broj_leta = input()
                        print("Polaziste: ")
                        polaziste = input()
                        print("Odrediste: ")
                        odrediste = input()
                        print("Vreme poletanja: ")
                        vreme_poletanja = input()
                        print("Vreme sletanja: ")
                        vreme_sletanja = input()
                        print("Sletanje sutra: ")
                        sletanje_sutra = input()
                        if sletanje_sutra == "False":
                            sletanje_sutra = False
                        elif sletanje_sutra == "True":
                            sletanje_sutra = True
                        print("Prevoznik: ")
                        prevoznik = input()
                        print("Dani(u formatu 1,2,3,4,...): ")
                        dani = input()
                        dani = dani.split(',')
                        for i in range(len(dani)):
                            dani[i] = int(dani[i])
                        print("Sifra modela: ")
                        sifra_modela = eval(input())
                        model = svi_modeli[sifra_modela]
                        print("Cena: ")
                        cena = input()
                        cena = float(cena)
                        print("Datum pocetka operativnosti: ")
                        datum_pocetka = input()
                        datum_pocetka = datetime.strptime(datum_pocetka, "%Y-%m-%d")
                        print("Datum kraja operativnosti: ")
                        datum_kraja = input()
                        datum_kraja = datetime.strptime(datum_kraja, "%Y-%m-%d")
                        svi_letovi = letovi.izmena_letova(svi_letovi, broj_leta, polaziste, odrediste, vreme_poletanja,
                                                          vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena,
                                                          datum_pocetka, datum_kraja)
                        remove_keys = []
                        for let in svi_konkretni_letovi:
                            if svi_konkretni_letovi[let]["broj_leta"] == broj_leta:
                                remove_keys.append(let)
                        for x in remove_keys:
                            del svi_konkretni_letovi[x]
                        svi_konkretni_letovi = konkretni_letovi.kreiranje_konkretnog_leta(svi_konkretni_letovi, svi_letovi[broj_leta])
                        for let in svi_konkretni_letovi:
                            if svi_konkretni_letovi[let]["broj_leta"] == broj_leta:
                                svi_konkretni_letovi[let]["zauzetost"] = letovi.podesi_matricu_zauzetosti(svi_letovi,svi_konkretni_letovi[let])
                        remove_keys.clear()
                        letovi.sacuvaj_letove("letovi.csv", "|", svi_letovi)
                        konkretni_letovi.sacuvaj_kokretan_let("konkretni_letovi.csv", "|", svi_konkretni_letovi)
                        for karta in sve_karte:
                            if sve_karte[karta]["sifra_konkretnog_leta"] not in svi_konkretni_letovi.keys():
                                remove_keys.append(karta)
                        for x in remove_keys:
                            del sve_karte[x]
                        sve_karte = karte.sacuvaj_karte(sve_karte, "karte.csv", "|")
                        print("Let i njegovi konkretni letovi su uspesno izmenjeni!")
                    except:
                        print("Doslo je do greske!")
                        continue
                case 11:
                    try:
                        print("Brojevi karata oznacenih za brisanje: ")
                        ind = 0
                        brojevi_brisanje = []
                        for karta in sve_karte:
                            if sve_karte[karta]["obrisana"] == True:
                                print(sve_karte[karta]["broj_karte"], " ", end="")
                                brojevi_brisanje.append(sve_karte[karta]["broj_karte"])
                                ind = 1
                        if ind != 0:
                            while True:
                                try:
                                    print("\nUnesite broj karte za brisanje: ")
                                    broj_karte = eval(input())
                                    if broj_karte not in brojevi_brisanje:
                                        print("Odabrana karta nije oznacena za brisanje!")
                                        continue
                                    break
                                except ValueError:
                                    print("Neispravan unos!!")
                                    continue
                            sve_karte = karte.brisanje_karte(korisnik, sve_karte, broj_karte)
                            karte.sacuvaj_karte(sve_karte, "karte.csv", "|")
                            print("Karta je uspesno obrisana!")
                        else:
                            print("Nema karata oznacenih za brisanje!")
                    except:
                        print("Doslo je do greske!")
                        continue
                case 12:
                    try:
                        print("Lista prodatih karata za izabrani dan prodaje - 1")
                        print("Lista prodatih karata za izabrani dan polaska - 2")
                        print("Lista prodatih karata za izabrani dan prodaje i izabranog prodavca - 3")
                        print("Ukupan broj i cena prodatih karata za izabrani dan prodaje - 4")
                        print("Ukupan broj i cena prodatih karata za izabrani dan polaska - 5")
                        print("Ukupan broj i cena prodatih karata za izabrani dan prodaje i izabranog prodavca - 6")
                        print("Uskupan broj i cena prodatih karata u poslednjih 30 dana, po prodavcima - 7")
                        while True:
                            try:
                                print("\nIzaberite vrstu izvestaja: ")
                                izbor_izvestaja = int(input())
                                if izbor_izvestaja < 1 or izbor_izvestaja > 7:
                                    print("Takav izvestaj ne postoji!")
                                    continue
                                break
                            except ValueError:
                                print("Takav izvestaj ne postoji!")
                                continue

                        match izbor_izvestaja:
                            case 1:
                                print("Unesite datum prodaje: ")
                                dan = input()
                                dan = datetime.strptime(dan, "%Y-%m-%d")
                                lista = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje(pom_karte, dan.date())
                                tabela_karte(karte_u_dict(lista))
                            case 2:
                                print("Unesite datum polaska: ")
                                dan = input()
                                dan = datetime.strptime(dan, "%Y-%m-%d")
                                lista = izvestaji.izvestaj_prodatih_karata_za_dan_polaska(pom_karte,
                                                                                          svi_konkretni_letovi,
                                                                                          dan.date())
                                tabela_karte(karte_u_dict(lista))
                            case 3:
                                print("Unesite datum prodaje: ")
                                dan = input()
                                dan = datetime.strptime(dan, "%Y-%m-%d")
                                print("Unesite korisnicko ime prodavca: ")
                                prodavac = input()
                                lista = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(pom_karte, dan,
                                                                                                     prodavac)
                                tabela_karte(karte_u_dict(lista))
                            case 4:
                                print("Unesite datum prodaje: ")
                                dan = input()
                                dan = datetime.strptime(dan, "%Y-%m-%d")
                                tapl = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje(pom_karte,
                                                                                             svi_konkretni_letovi,
                                                                                             svi_letovi, dan.date())
                                print("Broj: ", tapl[0], "\nCena: ", tapl[1])
                            case 5:
                                print("Unesite datum polaska: ")
                                dan = input()
                                dan = datetime.strptime(dan, "%Y-%m-%d")
                                tapl = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_polaska(pom_karte,
                                                                                             svi_konkretni_letovi,
                                                                                             svi_letovi, dan.date())
                                print("Broj: ", tapl[0], "\nCena: ", tapl[1])
                            case 6:
                                print("Unesite datum prodaje: ")
                                dan = input()
                                dan = datetime.strptime(dan, "%Y-%m-%d")
                                print("Unesite korisnicko ime prodavca: ")
                                prodavac = input()
                                tapl = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(pom_karte,
                                                                                                        svi_konkretni_letovi,
                                                                                                        svi_letovi,
                                                                                                        dan.date(),
                                                                                                        prodavac)
                                print("Broj: ", tapl[0], "\nCena: ", tapl[1])
                            case 7:
                                ubc30 = {}
                                ubc30 = izvestaji.izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(pom_karte,
                                                                                                     svi_konkretni_letovi,
                                                                                                     svi_letovi)
                                if ubc30 != {}:
                                    for elem in ubc30:
                                        print("\nBroj: ", ubc30[elem][0], "\nCena: ", ubc30[elem][1], "\nProdavac: ", ubc30[elem][2])
                                else:
                                    print("Nema prodatih karata u poslednjih 30 dana!")
                    except:
                        print("Doslo je do greske!")
                        continue
                case 13:
                    try:
                        print("Polaziste: ")
                        polaziste = input()
                        print("Odrediste: ")
                        odrediste = input()
                        print("Datum polaska: ")
                        datum_polaska = input()
                        if datum_polaska != "":
                            datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d")
                        else:
                             datum_polaska = None
                        lista = []
                        for let in svi_konkretni_letovi:
                            if svi_letovi[svi_konkretni_letovi[let]["broj_leta"]][
                                "sifra_polazisnog_aerodroma"] != polaziste and polaziste != "":
                                continue
                            if svi_letovi[svi_konkretni_letovi[let]["broj_leta"]][
                                "sifra_odredisnog_aerodorma"] != odrediste and odrediste != "":
                                continue
                            if datum_polaska != None and (svi_konkretni_letovi[let][
                                "datum_i_vreme_polaska"].year != datum_polaska.year or svi_konkretni_letovi[let][
                                "datum_i_vreme_polaska"].month != datum_polaska.month or svi_konkretni_letovi[let][
                                "datum_i_vreme_polaska"].day != datum_polaska.day):
                                continue
                            lista.append(svi_konkretni_letovi[let])

                        if len(lista) != 0:
                            konkretan_let = lista[0]
                            svaki_let = svi_letovi[konkretan_let["broj_leta"]]
                            sat_poletanja = svaki_let['vreme_poletanja'][:2]
                            minut_poletanja = svaki_let['vreme_poletanja'][3:]
                            sat_sletanja = svaki_let['vreme_sletanja'][:2]
                            minut_sletanja = svaki_let['vreme_sletanja'][3:]
                            vreme_letenja = timedelta(hours=int(sat_sletanja), minutes=int(minut_sletanja)) - timedelta(hours=int(sat_poletanja), minutes=int(minut_poletanja))
                            min = vreme_letenja
                            minl = []
                            minl.append(konkretan_let)
                            for i in range(1, len(lista)):
                                konkretan_let = lista[i]
                                svaki_let = svi_letovi[konkretan_let["broj_leta"]]
                                sat_poletanja = svaki_let['vreme_poletanja'][:2]
                                minut_poletanja = svaki_let['vreme_poletanja'][3:]
                                sat_sletanja = svaki_let['vreme_sletanja'][:2]
                                minut_sletanja = svaki_let['vreme_sletanja'][3:]
                                vreme_letenja = timedelta(hours=int(sat_sletanja), minutes=int(minut_sletanja)) - timedelta(hours=int(sat_poletanja), minutes=int(minut_poletanja))
                                if vreme_letenja <= min:
                                    min = vreme_letenja
                                    minl.append(lista[i])
                            tabela_konkretnih_letova(konvertuj_konkretne_u_dict(minl))
                        else:
                            print("Nema takvih letova!")
                    except:
                        print("Doslo je do greske!")
                        continue