from time import sleep

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


def sprawdz_czy_bylo_wszystko(rzuty:dict):
    byly = []

    for gracz, rzut in rzuty.items():
        if rzut not in byly:
            byly.append(rzut)

    # byly wszystkie rzuty
    if len(byly) >= 3:
        return True

    return False


def policz_punkty(rzuty: dict):
    punkty = {}
    lista_u = []

    for wartosc in rzuty.values():
        if wartosc not in lista_u:
            lista_u.append(wartosc)

    if len(lista_u) >= 3:
        return {}

    for gracz1, rzut1 in rzuty.items():
        punkty[gracz1] = 0

        if rzut1 is RZUT_KAMIEN:
            for gracz2, rzut2 in rzuty.items():
                if gracz2 is not gracz1 and rzut2 is not RZUT_PAPIER:
                    punkty[gracz1] += 1

        if rzut1 is RZUT_PAPIER:
            for gracz2, rzut2 in rzuty.items():
                if gracz2 is not gracz1 and rzut2 is not RZUT_NOZYCE:
                    punkty[gracz1] += 1

        if rzut1 is RZUT_NOZYCE:
            for gracz2, rzut2 in rzuty.items():
                if gracz2 is not gracz1 and rzut2 is not RZUT_KAMIEN:
                    punkty[gracz1] += 1

    punkty_znormalizowane = {}

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

    wszystko = False

    wszystkie_kombinacje = sprawdz_czy_bylo_wszystko(rzuty)

    # sprawdzamy czy nie ma remisu lub wszystkich kombinacji
    if len(wygrani) is len(rzuty) or wszystkie_kombinacje:
        wygrani = {'wszystkie kombinacje'}

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

def gra():
    gracze = ['Marek', 'Kamil', "Paweł",  'Sylwia']

    lista_graczy = {}
    wyniki = {}
    for gracz in gracze:
        dodaj_gracza(lista_graczy, gracz)
        wyniki[gracz] = 0

    # dopoki ktos nie wygral
    gramy = True
    while gramy:
        for gracz, wynik in wyniki.items():
            if wynik > 2:

                for gracz, punkty in wyniki.items():
                    if punkty >= 3:
                        print('\tWygrany: ', gracz,' [̲̅$̲̅(̲̅5̲̅)̲̅$̲̅]')
                return

            rzuty = runda(lista_graczy)
            print("Gracze wylosowali:")
            for gracz, rzut in rzuty.items():
                print(gracz + ': ' + RZUTY[rzut])

            print('------')
            print("Po punkcie zyskuja:")
            wygrani = policz_punkty(rzuty)
            if len(wygrani) is 0:
                print('remis lub wszystkie kombinacje')
            else:
                print(wygrani)
            try:
                for gracz, pkt in wygrani.items():
                    if gracz in wyniki:
                        wyniki[gracz] += 1
            except:
                pass

            print(wyniki)
            print('----------------')
            sleep(2)

        if not gramy:

            break

if __name__ == "__main__":
    # obsługa klawiatury
    from msvcrt import getch
    gra()
