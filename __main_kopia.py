'''
Author: Marek Malbrandt <marek.malbrandt@gmail.com>
'''

from time import sleep
from termcolor import colored

LICZBA_GRACZY = 5

MUZYCZKA_RUNDA = 'runda-gong.wav'
MUZYCZKA_PUNKT = 'score.wav'

punkty = 0

from random import randint as ri

RZUT_KAMIEN = 0
RZUT_NOZYCE = 1
RZUT_PAPIER = 2

RZUTY = {
    0: 'kamień',
    1: 'nożyce',
    2: 'papier',
}


def dodaj_gracza(lista_graczy: dict, imie):
    lista_graczy[imie] = {}


def runda(lista_graczy: dict):
    rzuty = {}

    # losowanie
    for gracz in lista_graczy.keys():
        rzuty[gracz] = ri(0, 2)

    return rzuty


def sprawdz_czy_bylo_wszystko(rzuty: dict):
    byly = []

    for gracz, rzut in rzuty.items():
        if rzut not in byly:
            byly.append(rzut)

    # byly wszystkie rzuty
    if len(byly) >= 3:
        return True

    return False


def pusc_muzyczke(param):
    import winsound

    winsound.PlaySound(param, winsound.SND_ASYNC)


def policz_punkty(rzuty: dict):
    punkty = {}
    lista_u = []

    for wartosc in rzuty.values():

        if wartosc not in lista_u:
            lista_u.append(wartosc)

    if len(lista_u) >= 3:
        return {}

    for gracz1, rzut1 in rzuty.items():
        czy_puscic = False
        punkty[gracz1] = 0

        if rzut1 is RZUT_KAMIEN:
            for gracz2, rzut2 in rzuty.items():
                if gracz2 is not gracz1 and rzut2 is not RZUT_PAPIER:
                    punkty[gracz1] += 1
                    czy_puscic = True

        if rzut1 is RZUT_PAPIER:
            for gracz2, rzut2 in rzuty.items():
                if gracz2 is not gracz1 and rzut2 is not RZUT_NOZYCE:
                    punkty[gracz1] += 1
                    czy_puscic = True


        if rzut1 is RZUT_NOZYCE:
            for gracz2, rzut2 in rzuty.items():
                if gracz2 is not gracz1 and rzut2 is not RZUT_KAMIEN:
                    punkty[gracz1] += 1
                    czy_puscic = True

        if czy_puscic:
            pusc_muzyczke(MUZYCZKA_PUNKT)


    max_punkty = policz_gracz_max_pkt(punkty)

    rzuty_txt = {}

    for gracz, rzut in rzuty.items():
        if rzut is RZUT_NOZYCE:
            rzuty_txt[gracz] = 'nozyce'

        if rzut is RZUT_KAMIEN:
            rzuty_txt[gracz] = 'kamien'

        if rzut is RZUT_PAPIER:
            rzuty_txt[gracz] = 'papier'

    # liczymy wyniki
    wygrani = {}
    for gracz, pkt in punkty.items():
        if pkt is max_punkty:
            wygrani[gracz] = 1

    wszystkie_kombinacje = sprawdz_czy_bylo_wszystko(rzuty)

    # sprawdzamy czy nie ma remisu lub wszystkich kombinacji
    if len(wygrani) is len(rzuty) or wszystkie_kombinacje:
        wygrani = {}

    return wygrani


def policz_gracz_max_pkt(punkty):
    max_gracz = next(iter(punkty.keys()))
    max_punkty = punkty[max_gracz]

    # szukamy gracza z max pkt
    for gracz, pkt in punkty.items():
        if pkt > max_punkty:
            max_gracz = gracz
            max_punkty = pkt

    return max_punkty


def wyswietl_graczy(wygrani:dict, z_punktami:bool = False):
    for imie, wynik in wygrani.items():
        do_wyswietlenia = "\t" + imie

        if z_punktami:
            do_wyswietlenia += ': ' + str(wynik)

        print(colored(do_wyswietlenia, 'white', attrs=['concealed']))


def kli_kla_klo(opoznienie):
    print('Kli...')
    sleep(opoznienie * 2)
    print('Kla...')
    sleep(opoznienie * 2)
    print('Klo!')

def gra(gracze, do_ilu = 3, przerwa_sekundy = 2, opoznienie = 0.250):

    lista_graczy = {}
    wyniki = {}
    nr_rundy = 1

    # dodajemy graczy
    for gracz in gracze:
        dodaj_gracza(lista_graczy, gracz)
        wyniki[gracz] = 0

    # dopoki ktos nie wygral
    gramy = True
    wygrana = False
    while gramy:
        pusc_muzyczke('runda-gong.wav')
        print('----------------------------')
        print(colored(('Runda nr: '+str(nr_rundy)), color='white', attrs=['dark', 'bold']))
        nr_rundy += 1
        rzuty = runda(lista_graczy)

        kli_kla_klo(opoznienie)

        # wyświetlamy rzuty graczy
        print(colored("Gracze wylosowali:", 'green'))
        sleep(opoznienie)
        wyswietl_rzuty(rzuty)

        sleep(opoznienie)
        print(colored("Po punkcie zyskuja:", 'blue'))
        wygrani = policz_punkty(rzuty)
        sleep(opoznienie)
        if len(wygrani) is 0:
            print(colored("\tremis lub wszystkie kombinacje", 'red'))
        else:
            if len(wygrani) > 0:
                wyswietl_graczy(wygrani)
        try:
            wyniki = policz_wyniki(wygrani, wyniki)
        except:
            pass

        print(colored('Obecna punktacja:', 'cyan'))
        wyswietl_graczy(wyniki, True)

        for imie, wynik in wyniki.items():
            if wynik >= 3:
                sleep(opoznienie)
                pusc_muzyczke('ta-da.wav')
                print(colored('***** WYGRANA *****', 'red'))
                wyswietl_wygranych(wyniki, do_ilu)
                gramy = False
                break

        sleep(przerwa_sekundy)

        if not gramy:
            break


def policz_wyniki(wygrani, wyniki):
    for gracz, pkt in wygrani.items():
        if gracz in wyniki:
            wyniki[gracz] += 1

    return wyniki


def wyswietl_rzuty(rzuty):
    for gracz, rzut in rzuty.items():
        print("\t", colored(gracz + ': ' + RZUTY[rzut], 'white'))


def wyswietl_wygranych(wyniki, wygrywa_pkt = 3):
    for gracz, punkty in wyniki.items():
        if punkty >= wygrywa_pkt:
            print('\tWygrany: ', colored(gracz, 'magenta'), colored(' [̲̅$̲̅(̲̅5̲̅)̲̅$̲̅]', 'green'))


if __name__ == "__main__":
    # obsługa klawiatury
    from msvcrt import getch
    gracz_prefix = 'gracz_'
    gracze = []

    # for i in range(0, LICZBA_GRACZY):
    #     gracze.append('gracz_' + str(i))

    gracze = ['Marek', 'Paweł', 'Sylwia']
    gra(gracze)
