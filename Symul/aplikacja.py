# Autor: Paweł Deptuła
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from PIL import Image, ImageTk
import sys
from idlelib.tooltip import Hovertip
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os 
# Ustawienie czcionki do generowania tekstu z obsluga polskich znaków
sciezka = os.getcwd()
pdfmetrics.registerFont(TTFont('DejaVu',sciezka+ '/DejaVuSans.ttf'))
root = Tk()
root.title("Symulacja pożaru lasu - Paweł Deptuła")
middle_frame =[]
root.geometry("1920x1080")
root.resizable(False, False)
root.columnconfigure(0, weight = 8, uniform = 'a')
root.columnconfigure((1,2,3), weight = 1, uniform = 'a')

root.rowconfigure((0,1), weight = 1, uniform = 'a')

#przycisk = Button(root, text="Start", command=start_simulation)
frame_parametry = Frame(root)  # Opcjonalnie dodano kolor tła dla widoczności
#frame.pack(side="right", padx=0, pady=0)  # Frame wyrównany do prawej strony
zdjecie_frame =Frame(root,background="grey")  # Opcjonalnie dodano kolor tła dla widoczności
zdjecie_frame.grid(row=0,rowspan=2, column=0, sticky="nsew") 
zdjecie_frame.columnconfigure(0, weight = 1, uniform = 'a')
zdjecie_frame.rowconfigure(0, weight = 1, uniform = 'a')
frame_parametry.grid(row=0, column=1,columnspan=3, sticky="nsew")


# Umieszczenie ramki w siatce (np. od kolumny 1 do 3 i od wiersza 2 do 4)
#root.mainloop()
Pozycja_pol_x = 5
Pozycja_pol_y = 5

frame_parametry.columnconfigure(0, weight = 1, uniform = 'a')
frame_parametry.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16), weight = 1, uniform = 'a')
frame_parametry.grid_propagate(False)
napis = Label(frame_parametry, text="Parametry symulacji",width=25, height=5, font=("Arial", 12))
napis.grid(row=0, column=0,padx=5, pady=5, sticky="n")

#root.mainloop()
# funkcja dodająca pole tekstowe oraz pola do wprowadzania 
def dodaj_pole(opis, domyslna_wartosc, wiersz,kotwica="nw"):
    Label(frame_parametry, text=opis, anchor=kotwica, width=45).grid(row=wiersz, column=0, padx=0, pady=0, sticky="w")
    var = StringVar(value=str(domyslna_wartosc))
    pole = Entry(frame_parametry, width=10, textvariable=var)
    pole.grid(row=wiersz, column=0, padx=Pozycja_pol_x, pady=Pozycja_pol_y,sticky="e")
    return pole
Holder_grid = []
obrazki_symulacji = {
    1: sciezka+"/pola/puste_pole.png",
    2: sciezka+"/pola/drzewo.png",
    3: sciezka+"/pola/woda.png",
    4: sciezka+"/pola/plonoce_drzewo.png",
    5: sciezka+"/pola/spalone_drzewo.png",
    6: sciezka+"/pola/lawa.png",
}
def sklasyfikuj_wiatr(wektor):# 1 współczynnik to x 2 współczynnik to y
    if(wektor == (0,-1)):
        return "Północ"
    if(wektor == (1,0)):
        return "Wschód"
    if(wektor == (0,1)):
        return "Południe"
    if(wektor == (-1,0)):
        return "Zachód"
    if(wektor == (1,-1)):
        return "Północny wschód"
    if(wektor == (-1,-1)):
        return "Północny zachód"
    if(wektor == (-1,1)):
        return "Południowy zachód"
    if(wektor == (1,1)):
        return "Południowy wschód"

global info,puste, drzewo, woda, plo_drzewo, spal_drzewo, lawa
info,puste, drzewo, woda, plo_drzewo, spal_drzewo, lawa,wiatr = StringVar(),StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(),StringVar()

def zmiana_obrazu(wartosc):
    # Aktualizacja obrazu
    T =konwertuj_macierz_na_obraz(Holder_grid[wartosc], obrazki_symulacji, zdjecie_frame)
    # Aktualizacja wartości StringVar
    info.set(f"Informacje o iteracji nr {wartosc}")
    puste.set(f'Ilość {STANY1[0]} NA obecnej iteracji: {wydobadz_dane_z_gridu(Holder_grid[wartosc])[STANY[0]]}')
    drzewo.set(f'Ilość {STANY1[1]} NA obecnej iteracji: {wydobadz_dane_z_gridu(Holder_grid[wartosc])[STANY[1]]}')
    woda.set(f'Ilość {STANY1[2]} NA obecnej iteracji: {wydobadz_dane_z_gridu(Holder_grid[wartosc])[STANY[2]]}')
    plo_drzewo.set(f'Ilość {STANY1[3]} NA obecnej iteracji: {wydobadz_dane_z_gridu(Holder_grid[wartosc])[STANY[3]]}')
    spal_drzewo.set(f'Ilość {STANY1[4]} NA obecnej iteracji: {wydobadz_dane_z_gridu(Holder_grid[wartosc])[STANY[4]]}')
    lawa.set(f'Ilość {STANY1[5]} NA obecnej iteracji: {wydobadz_dane_z_gridu(Holder_grid[wartosc])[STANY[5]]}')
    wiatr.set(f"Obecny kierunek wiatru :{sklasyfikuj_wiatr(Holder_wiatru[wartosc])}")
    # wymuś aktualizacje 
    root.update_idletasks()
def zmniejsz_iteracje():
    global suwak_wartosc
    wartosc = suwak_wartosc.get() - 1
    if wartosc >= 0:
        suwak_wartosc.set(wartosc)
        zmiana_obrazu(wartosc)
        #print(suwak_wartosc.get())
        slider.set(wartosc)
def zwieksz_iteracje():
    global suwak_wartosc
    wartosc = suwak_wartosc.get() + 1
    if wartosc <= len(Holder_grid)-1:
        suwak_wartosc.set(wartosc)
        zmiana_obrazu(wartosc)
        slider.set(wartosc)
def ustaw_iteracje(wartosc):
    global suwak_wartosc
    suwak_wartosc.set(wartosc)
    zmiana_obrazu(suwak_wartosc.get())
def dane_z_gridu(grid):
    global frame_opis_iteracji, puste, drzewo, woda, plo_drzewo, spal_drzewo, lawa
    slownik = wydobadz_dane_z_gridu(Holder_grid[len(Holder_grid) - 1])
    # Ustawienie początkowych wartości StringVar
    info.set(f"Informacje o iteracji nr {len(Holder_grid)-1}")
    puste.set(f'Ilość {STANY1[0]} NA obecnej iteracji: {slownik[STANY[0]]}')
    drzewo.set(f'Ilość {STANY1[1]} NA obecnej iteracji: {slownik[STANY[1]]}')
    woda.set(f'Ilość {STANY1[2]} NA obecnej iteracji: {slownik[STANY[2]]}')
    plo_drzewo.set(f'Ilość {STANY1[3]} NA obecnej iteracji: {slownik[STANY[3]]}')
    spal_drzewo.set(f'Ilość {STANY1[4]} NA obecnej iteracji: {slownik[STANY[4]]}')
    lawa.set(f'Ilość {STANY1[5]} NA obecnej iteracji: {slownik[STANY[5]]}')
    wiatr.set(f"Obecny kierunek wiatru :{sklasyfikuj_wiatr(Holder_wiatru[len(Holder_wiatru) - 1])}")
    frame_opis_iteracji = Frame(root)
    frame_opis_iteracji.grid(row=1, column=1,columnspan=3, sticky="nsew")
    # ustawienie zmiennej domyslnie na ostatnia iteracje 
    suwak_wartosc.set(len(Holder_grid) - 1)
    global slider
    # Slider do zmiany iteracji 
    slider = Scale(frame_opis_iteracji, from_=0, to=len(Holder_grid) - 1, orient=HORIZONTAL, command=ustaw_iteracje)
    slider.set(len(Holder_grid) - 1)
    slider.pack(side=BOTTOM, padx=5,fill='both')  # Umieszczenie od lewa do prawa
    # 
    przycisk_zmniejsz = Button(frame_opis_iteracji, text="Poprzednia iteracja", font=("Arial", 12), command=zmniejsz_iteracje, width=20, height=2)
    przycisk_zmniejsz.pack(side=BOTTOM, padx=5,fill='both')  # Umieszczenie od lewa do prawa 
    
    przycisk_zwieksz = Button(frame_opis_iteracji, text="Następna iteracja", font=("Arial", 12), command=zwieksz_iteracje, width=20, height=2)
    przycisk_zwieksz.pack(side=BOTTOM, padx=5,fill='both')  # Umieszczenie od lewa do prawa
    
    # Etykiety
    Label(frame_opis_iteracji, textvariable=info, font=("Arial", 12)).pack(pady=5)
    Label(frame_opis_iteracji, textvariable=puste, font=("Arial", 12)).pack(pady=5)
    Label(frame_opis_iteracji, textvariable=drzewo, font=("Arial", 12)).pack(pady=5)
    Label(frame_opis_iteracji, textvariable=woda, font=("Arial", 12)).pack(pady=5)
    Label(frame_opis_iteracji, textvariable=plo_drzewo, font=("Arial", 12)).pack(pady=5)
    Label(frame_opis_iteracji, textvariable=spal_drzewo, font=("Arial", 12)).pack(pady=5)
    Label(frame_opis_iteracji, textvariable=lawa, font=("Arial", 12)).pack(pady=5)
    # Dodanie etykiety z kierunkiem wiatru
    Label(frame_opis_iteracji, textvariable=wiatr, font=("Arial", 12)).pack(pady=5)
    if(int(ILOSC_ITERACJI.get())>len(Holder_grid)):
        wynik = "Symulacja zakończona, spłoneło ostatnie z płonących drzew"
    else:
        wynik = "Symulacja zakończona, osiągnieto limit iteracji"
    Label(frame_opis_iteracji,text=wynik,font=("Arial", 12)).pack(pady=5)
    Button(frame_opis_iteracji,text="Wygeneruj raport",font=("Arial", 12),bg="blue",command=generuj_raport).pack(pady=10)
    global label_sukces_raport_generacja
    global napis_sukces_gen
    napis_sukces_gen= StringVar(root,"")
    label_sukces_raport_generacja = Label(frame_opis_iteracji, textvariable=napis_sukces_gen, bg="green")
    label_sukces_raport_generacja.pack_forget()
# Zmienna przechowująca aktualną iterację
suwak_wartosc = IntVar(root, len(Holder_grid) - 1)
def zaladuj_obrazki(image_map, size):
    slownik_obrazki = {}
    for key, path in image_map.items(): # Iteracja po kluczach i ścieżkach obrazków
        img = Image.open(path).resize(size,Image.Resampling.NEAREST) # Otwarcie obrazka i zmiana rozmiaru
        slownik_obrazki[key] = ImageTk.PhotoImage(img) # Przypisanie obrazka do klucza
    return slownik_obrazki
# funkcja resetujaca aktualne widgety
def resetuj():
    global HOLDER_KANWY
    HOLDER_KANWY = []  # Resetowanie obrazów na Canvas
    for widget in zdjecie_frame.winfo_children():  # Resetowanie wszystkich widgetów w ramce
        widget.destroy()
    if 'frame_opis_iteracji' in globals() and type(frame_opis_iteracji) == Frame: 
        frame_opis_iteracji.destroy()
def generuj_raport():
    # Pobranie danych z pól tekstowych
    ilosc_iteracji = int(ILOSC_ITERACJI.get())
    rozmiar_siatki = int(ROZMIAR_SIATKI.get())
    p_zaplonu_od_sasiada = float(P_ZAPLONU_OD_SASIADA.get())
    p_samozaplonu = float(P_SAMOZAPLONU.get())
    czas_odnowienia_drzewa = int(CZAS_ODNOWIENIA_DRZEWA.get())
    czestotliwosc_zmiany_wiatru = int(CZESTOTLIWOSC_ZMIANY_KIERUNKU_WIATRU.get())
    wskaznik_wzrostu_rozprzestrzeniania = int(WSKAZNIK_WZROSTU_ROZPRZESTRZENIANIA.get())
    proporcja_drzew = float(PROPORCJA_DRZEW.get())
    proporcja_pustych_pol = float(PROPORCJA_PUSTYCH_POL.get())
    proporcja_wody = float(PROPORCJA_WODY.get())
    proporcja_lawy = float(PROPORCJA_LAWY.get())
    wskaznik_erupcji_lawy = float(WSKAZNIK_ERUPCJI_LAWY.get())
    wskaznik_rozprzestrzeniania_sadzonek = float(WSKAZNIK_ROZPRZESTRZENIANIA_SADZONEK.get())
    wskaznik_wygaszania_lawy = float(WSKAZNIK_WYGASZANIA_LAWY.get())
    p_zaplonu_od_lawy = float(P_ZAPLONU_OD_LAWY.get())
    szansa_na_odrodzenie_drzewa = float(SZANSA_NA_ODRODZENIE_DRZEWA.get())
    # Generowanie wykresu przedstawiajacego proporcje 
    iteracje = list(range(1, len(Holder_grid) + 1))
    plt.figure(figsize=(8, 6))
    slownik_danych_z_gridu = {}
    for a in STANY:
        slownik_danych_z_gridu[a]=[]
        for x in Holder_grid:
            holder_danych_z_gridu = wydobadz_dane_z_gridu(x)
            slownik_danych_z_gridu[a].append(holder_danych_z_gridu[a])
    # Sprawdź długość danych i iteracji
    #for a in STANY:
        #print(len(slownik_danych_z_gridu[a]), len(iteracje))

    # Rysowanie wykresu
    plt.plot(iteracje, slownik_danych_z_gridu[1], label=STANY1[1-1], color="grey")
    plt.plot(iteracje, slownik_danych_z_gridu[2], label=STANY1[2-1], color="green")
    plt.plot(iteracje, slownik_danych_z_gridu[3], label=STANY1[3-1], color="blue")
    plt.plot(iteracje, slownik_danych_z_gridu[4], label=STANY1[4-1], color="red")
    plt.plot(iteracje, slownik_danych_z_gridu[5], label=STANY1[5-1], color="black")
    plt.plot(iteracje, slownik_danych_z_gridu[6], label=STANY1[6-1], color="purple") 
    # ustawienia wykresu
    plt.xlabel("Iteracja")
    plt.ylabel("Wartość")
    plt.title("Wykres opisujący przebieg symulacji")
    plt.legend()
    plt.grid()
    plt.savefig(sciezka+f"/wykresy/wykres_{1}.png")
    plt.close()

    # Tworzenie raportu PDF
    nazwa_raportu = f"raport_pozaru_lasu_{random.random()}.pdf"
    pdf = canvas.Canvas(sciezka+"/raporty/"+nazwa_raportu, pagesize=A4)
    # pobranie szerokosci i wysokosci formatu pdf
    szerokosc, wysokosc = A4
    # ustawienie customowej czcionki
    pdf.setFont("DejaVu", 15)
    # Tytuł raportu
    pdf.drawString(50, wysokosc - 50, "Raport z symulacji pożaru lasu")
    # Początkowe parametry
    pdf.setFont("DejaVu", 13)
    if(int(ILOSC_ITERACJI.get())>len(Holder_grid)):
        wynik = "spłoneło ostatnie z płonących drzew"
    else:
        wynik = "osiągnieto limit iteracji"
    ostateczna_ilosc_iteracji = len(Holder_grid) - 1 
    params = [
        f"Parametry startowe",
        f"Ilość maksymalna iteracji: {ilosc_iteracji}",
        f"Rozmiar siatki: {rozmiar_siatki}",
        f"Prawdopodobieństwo zapłonu od sąsiada: {p_zaplonu_od_sasiada}",
        f"Prawdopodobieństwo samozapłonu: {p_samozaplonu}",
        f"Czas odnowienia drzewa: {czas_odnowienia_drzewa}",
        f"Częstotliwość zmiany kierunku wiatru: {czestotliwosc_zmiany_wiatru}",
        f"Wskaźnik wzrostu rozprzestrzeniania: {wskaznik_wzrostu_rozprzestrzeniania}",
        f"Proporcja drzew: {proporcja_drzew}",
        f"Proporcja pustych pól: {proporcja_pustych_pol}",
        f"Proporcja wody: {proporcja_wody}",
        f"Proporcja lawy: {proporcja_lawy}",
        f"Wskaźnik erupcji lawy: {wskaznik_erupcji_lawy}",
        f"Wskaźnik rozprzestrzeniania sadzonek: {wskaznik_rozprzestrzeniania_sadzonek}",
        f"Wskaźnik wygaszania lawy: {wskaznik_wygaszania_lawy}",
        f"Prawdopodobieństwo zapłonu od lawy: {p_zaplonu_od_lawy}",
        f"Szansa na odrodzenie drzewa: {szansa_na_odrodzenie_drzewa}"," " ,
        f"Wyniki:",
        f"Ostateczna ilosc iteracji:{  ostateczna_ilosc_iteracji }",
        f"Rezultat symulacji: {wynik}"
    ]
    y = wysokosc - 100
    for param in params:
        pdf.drawString(50, y, param)
        y -= 20
    # Dodanie wykresu do raportu
    pdf.drawImage(sciezka+f"/wykresy/wykres_{1}.png", 50, y - 300, width=500, height=300)

    # Zakończenie tworzenia PDF
    pdf.save()
    print(f"Raport został wygenerowany jako{nazwa_raportu}")
    napis_sukces_gen.set(f"Raport został wygenerowany jako: {nazwa_raportu}")
    label_sukces_raport_generacja.pack(pady=5)
def konwertuj_macierz_na_obraz(grid,obrazki,frame):
    # Usunięcie wszystkich widgetów z ramki jesli istnieja ( dla odswiezenia )
    for widget in frame.winfo_children():
        widget.destroy()
    # Pobranie szerokości i wysokości ramki
    szerokosc_frame = zdjecie_frame.winfo_width()
    wysokosc_frame = zdjecie_frame.winfo_height()
    # ustawienie by tkinter nie zmieniał rozmiaru ramki 
    zdjecie_frame.grid_propagate(False)
    # Rozmiar punktu na siatce (w pikselach) ( rozmiar ramki dzielony przez rozmiar gridu)
    rozmiar_punktux,rozmiar_punktuy = (szerokosc_frame // len(grid[0]), wysokosc_frame // len(grid))
    # Utworzenie płótna o odpowiednich wymiarach 
    canvas = Canvas(zdjecie_frame,width=szerokosc_frame, height=wysokosc_frame) 
    # Ustawienie płótna w ramce za pomoca pack 
    canvas.pack()
    # Zaladowanie obrazków i przeskalowanie ich do odpowiedniego rozmiaru 
    images = zaladuj_obrazki(obrazki, (rozmiar_punktux,rozmiar_punktuy))
    # zmienna globalna przechowujaca kanwy ( musi byc globalna bo tkinter inacjej nie widzi)
    global HOLDER_KANWY
    HOLDER_KANWY = []   
    # iteracja po wszystkich komórkach 
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            # pobranie zdjecia po wartosci pola 
            img = images.get(value)
            if img:
                # umieszczenie obiektu na płótnie, o rozmiarach 1/(szerokosc_ramki/rozmiar_gridu)
                canvas.create_image(j * rozmiar_punktux, i * rozmiar_punktuy, anchor=NW, image=img)
                HOLDER_KANWY.append(img)
    # wymus aktualizacje gui
    root.update_idletasks()
    return canvas

# Dodawanie pól tekstowych do wprowadzania parametrów
ILOSC_ITERACJI = dodaj_pole("Maksymalna ilość iteracji:", 100, 1)
ROZMIAR_SIATKI = dodaj_pole("Rozmiar siatki:", 25, 2)
P_ZAPLONU_OD_SASIADA = dodaj_pole("Prawdopodobieństwo zapłonu od sąsiada(%):", 0.4, 3)
P_SAMOZAPLONU = dodaj_pole("Prawdopodobieństwo samozapłonu(%):", 0.05, 4)
P_ZAPLONU_OD_LAWY = dodaj_pole("Prawdopodobieństwo zapłonu od lawy(%):", 0.1, 5)
CZAS_ODNOWIENIA_DRZEWA = dodaj_pole("Czas odnowienia drzewa(ITERACJE):", 10, 6)
CZESTOTLIWOSC_ZMIANY_KIERUNKU_WIATRU = dodaj_pole("Częstotliwość zmiany kierunku wiatru(ITERACJE):", 5, 7)
WSKAZNIK_WZROSTU_ROZPRZESTRZENIANIA = dodaj_pole("Wskaźnik wzrostu rozprzestrzeniania poprzez wiatr(RAZY):", 2, 8)
WSKAZNIK_ROZPRZESTRZENIANIA_SADZONEK = dodaj_pole("Wskaźnik rozprzestrzeniania sadzonek():", 0.05, 9)
WSKAZNIK_ERUPCJI_LAWY = dodaj_pole("Wskaźnik erupcji lawy(%):", 0.01, 10)
PROPORCJA_DRZEW = dodaj_pole("Proporcja drzew(%):", 0.8, 11)
PROPORCJA_PUSTYCH_POL = dodaj_pole("Proporcja pustych pól(%):", 0.1, 12)
PROPORCJA_WODY = dodaj_pole("Proporcja wody (%):", 0.05, 13)
PROPORCJA_LAWY = dodaj_pole("Proporcja lawy(%):", 0.05, 14)
WSKAZNIK_WYGASZANIA_LAWY = dodaj_pole("Wskaźnik wygaszania lawy(%):", 5, 15)
WEKTORY_KIERUNKU_WIATRU = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
SZANSA_NA_ODRODZENIE_DRZEWA = dodaj_pole("Szansa na odrodzenie drzewa(%):", 0.1, 16)
PROPORCJE=[PROPORCJA_DRZEW,PROPORCJA_PUSTYCH_POL,PROPORCJA_WODY,PROPORCJA_LAWY]

# DEKLARACJA STANÓW KOMÓREK
PUSTY = 1
DRZEWO = 2
WODA = 3
PLONACE_DRZEWO = 4
SPALONE_DRZEWO = 5
LAWA = 6

# Funkcja do wyciagania danych o komórkach z gridu
def wydobadz_dane_z_gridu(grid):
    x = {}
    for j in STANY:
        x[j] = 0
    for t in range(len(grid)):
        for y in range(len(grid)):
            x[grid[t][y]] += 1
    return x
# Dodanie tooltipa aby wyswietlac bledy przy parametrach


# Główna funkcja projektu 
def Symulacja():
    resetuj()
    # Pobranie wartości z pól tekstowych
    ilosc_iteracji = int(ILOSC_ITERACJI.get())
    rozmiar_siatki = int(ROZMIAR_SIATKI.get())
    p_zaplonu_od_sasiada = float(P_ZAPLONU_OD_SASIADA.get())
    p_samozaplonu = float(P_SAMOZAPLONU.get())
    czas_odnowienia_drzewa = int(CZAS_ODNOWIENIA_DRZEWA.get())
    czestotliwosc_zmiany_wiatru = int(CZESTOTLIWOSC_ZMIANY_KIERUNKU_WIATRU.get())
    wskaznik_wzrostu_rozprzestrzeniania = int(WSKAZNIK_WZROSTU_ROZPRZESTRZENIANIA.get())
    proporcja_drzew = float(PROPORCJA_DRZEW.get())
    proporcja_pustych_pol = float(PROPORCJA_PUSTYCH_POL.get())
    proporcja_wody = float(PROPORCJA_WODY.get())
    proporcja_lawy = float(PROPORCJA_LAWY.get())
    wskaznik_erupcji_lawy = float(WSKAZNIK_ERUPCJI_LAWY.get())
    wskaznik_rozprzestrzeniania_sadzonek = float(WSKAZNIK_ROZPRZESTRZENIANIA_SADZONEK.get())
    wskaznik_wygaszania_lawy = float(WSKAZNIK_WYGASZANIA_LAWY.get())
    p_zaplonu_od_lawy = float(P_ZAPLONU_OD_LAWY.get())
    szansa_na_odrodzenie_drzewa = float(SZANSA_NA_ODRODZENIE_DRZEWA.get())

    # Sekcja do sprawdzania poprawności wprowadzonych danych
    # wartosci maja dedykowana instrukcje warunktowa by zmienic kolor na czerwony tylko tej która jest nie poprawna
    # sprawdzenie czy suma proporcji wynosi 1
    if(proporcja_drzew + proporcja_pustych_pol + proporcja_wody + proporcja_lawy != 1):
        PROPORCJA_DRZEW.config(bg="red") # zamiana koloru na czerwony 
        PROPORCJA_PUSTYCH_POL.config(bg="red")
        PROPORCJA_WODY.config(bg="red")
        PROPORCJA_LAWY.config(bg="red")
        Hovertip(PROPORCJA_DRZEW, "Suma proporcji musi wynosic 1")
        Hovertip(PROPORCJA_PUSTYCH_POL, "Suma proporcji musi wynosic 1")
        Hovertip(PROPORCJA_WODY, "Suma proporcji musi wynosic 1")
        Hovertip(PROPORCJA_LAWY, "Suma proporcji musi wynosic 1")
        raise ValueError("Suma proporcji musi wynosic 1")
    # Sprawdzenie czy ilosc iteracji
    if(ilosc_iteracji <= 0 or ilosc_iteracji > 1000):
        ILOSC_ITERACJI.config(bg="red")
        Hovertip(ILOSC_ITERACJI, "Maksymalna ilość iteracji musi byc wieksza od 0 i mniejsza od 1000")
        raise ValueError("Ilosc iteracji musi byc wieksza od 0 i mniejsza od 1000")
    # Sprawdzenie czy rozmiar siatki jest wiekszy od 0
    if(rozmiar_siatki <= 0 or rozmiar_siatki > 100):
        ROZMIAR_SIATKI.config(bg="red")
        Hovertip(ROZMIAR_SIATKI, "Rozmiar siatki musi byc wiekszy od 0 i mniejszy od 100")
        raise ValueError("Rozmiar siatki musi byc wiekszy od 0")
    # Sprawdzenie czy wartości są większe od 0
    if(p_zaplonu_od_sasiada < 0  or p_zaplonu_od_sasiada > 1):
        P_ZAPLONU_OD_SASIADA.config(bg="red")
        Hovertip(P_ZAPLONU_OD_SASIADA, "Wartości zaplonu od sasiada muszą być większe lub równe 0 i mniejsze od 1")
        raise ValueError("Wartości zaplonu od sasiada muszą być większe od 0") 
    if(p_samozaplonu < 0 or p_samozaplonu > 1):
        P_SAMOZAPLONU.config(bg="red")
        Hovertip(P_SAMOZAPLONU, "Wartości samozaplonu muszą być większe lub równe 0 i mniejsze od 1")
        raise ValueError("Wartości samozaplonu muszą być większe od 0")
    if(czas_odnowienia_drzewa <= 0):
        CZAS_ODNOWIENIA_DRZEWA.config(bg="red")
        Hovertip(CZAS_ODNOWIENIA_DRZEWA, "Czas odnowienia drzewa musi być większy od 0")
        raise ValueError("Czas odnowienia drzewa musi być większy od 0")
    if(czestotliwosc_zmiany_wiatru < 0):
        CZESTOTLIWOSC_ZMIANY_KIERUNKU_WIATRU.config(bg="red")
        Hovertip(CZESTOTLIWOSC_ZMIANY_KIERUNKU_WIATRU, "Częstotliwość zmiany kierunku wiatru musi być większa lub równa 0")
        raise ValueError("Częstotliwość zmiany kierunku wiatru musi być większa od 0")
    if(wskaznik_wzrostu_rozprzestrzeniania < 0):
        WSKAZNIK_WZROSTU_ROZPRZESTRZENIANIA.config(bg="red")
        Hovertip(WSKAZNIK_WZROSTU_ROZPRZESTRZENIANIA, "Wskaźnik wzrostu rozprzestrzeniania musi być większy lub równy 0")
        raise ValueError("Wskaźnik wzrostu rozprzestrzeniania musi być większy od 0")
    if(wskaznik_erupcji_lawy < 0 or wskaznik_erupcji_lawy > 1):
        WSKAZNIK_ERUPCJI_LAWY.config(bg="red")
        Hovertip(WSKAZNIK_ERUPCJI_LAWY, "Wskaźnik erupcji lawy musi być większy lub równy 0 i mniejszy od 1")
        raise ValueError("Wskaźnik erupcji lawy musi być większy od 0")
    if(proporcja_lawy < 0 or proporcja_lawy > 1):
        PROPORCJA_LAWY.config(bg="red")
        Hovertip(PROPORCJA_LAWY, "Proporcja lawy musi być większa lub równa 0 i mniejsza od 1")
        raise ValueError("Proporcja lawy musi być większa od 0")
    if(proporcja_pustych_pol < 0 or proporcja_pustych_pol > 1):
        PROPORCJA_PUSTYCH_POL.config(bg="red")
        Hovertip(PROPORCJA_PUSTYCH_POL, "Proporcja pustych pól musi być większa lub równa 0 i mniejsza od 1")
        raise ValueError("Proporcja pustych pól musi być większa od 0")
    if(proporcja_wody < 0 or proporcja_wody > 1):
        PROPORCJA_WODY.config(bg="red")
        Hovertip(PROPORCJA_WODY, "Proporcja wody musi być większa lub równa 0 i mniejsza od 1")
        raise ValueError("Proporcja wody musi być większa od 0")
    if(proporcja_drzew < 0 or proporcja_drzew > 1):
        PROPORCJA_DRZEW.config(bg="red")
        Hovertip(PROPORCJA_DRZEW, "Proporcja drzew musi być większa lub równa 0 i mniejsza od 1")
        raise ValueError("Proporcja drzew musi być większa od 0")
    if(wskaznik_rozprzestrzeniania_sadzonek < 0 or wskaznik_rozprzestrzeniania_sadzonek > 1):
        WSKAZNIK_ROZPRZESTRZENIANIA_SADZONEK.config(bg="red")
        Hovertip(WSKAZNIK_ROZPRZESTRZENIANIA_SADZONEK, "Wskaźnik rozprzestrzeniania sadzonek musi być większy lub równy 0 i mniejszy od 1")
        raise ValueError("Wskaźnik rozprzestrzeniania sadzonek musi być większy od 0")
    if(wskaznik_wygaszania_lawy <0):
        WSKAZNIK_WYGASZANIA_LAWY.config(bg="red")
        Hovertip(WSKAZNIK_WYGASZANIA_LAWY, "Wskaźnik wygaszania lawy musi być większy lub równy 0")
        raise ValueError("Wskaźnik wygaszania lawy musi być większy od 0")
    if(p_zaplonu_od_lawy < 0 or p_zaplonu_od_lawy > 1):
        P_ZAPLONU_OD_LAWY.config(bg="red")
        Hovertip(P_ZAPLONU_OD_LAWY, "Prawdopodobieństwo zapłonu od lawy musi być większe lub równy 0 i mniejsze od 1")
        raise ValueError("Prawdopodobieństwo zapłonu od lawy musi być większe od 0")
    if(szansa_na_odrodzenie_drzewa < 0 or szansa_na_odrodzenie_drzewa > 1):
        SZANSA_NA_ODRODZENIE_DRZEWA.config(bg="red")
        Hovertip(SZANSA_NA_ODRODZENIE_DRZEWA, "Szansa na odrodzenie drzewa musi być większa lub równa 0 i mniejsza od 1")
        raise ValueError("Szansa na odrodzenie drzewa musi być większa od 0")
    
    proporcje = [proporcja_pustych_pol,proporcja_drzew,proporcja_wody,proporcja_lawy]
    # wyswietlenie w konsoli wybrancych parametrów
    print("Parametry symulacji:")
    print(f"Rozmiar siatki: {rozmiar_siatki}")
    print(f"Prawdopodobieństwo zapłonu od sąsiada: {p_zaplonu_od_sasiada}")
    print(f"Prawdopodobieństwo samozapłonu: {p_samozaplonu}")
    print(f"Czas odnowienia drzewa: {czas_odnowienia_drzewa}")
    print(f"Częstotliwość zmiany kierunku wiatru: {czestotliwosc_zmiany_wiatru}")
    print(f"Proporcja drzew: {proporcja_drzew}")
    print(f"Proporcja pustych pól: {proporcja_pustych_pol}")
    print(f"Proporcja wody: {proporcja_wody}")
    print(f"Proporcja lawy: {proporcja_lawy}")
    print(f"Wskaźnik erupcji lawy: {wskaznik_erupcji_lawy}")
    print(f"Wskaźnik rozprzestrzeniania sadzonek: {wskaznik_rozprzestrzeniania_sadzonek}")
    print(f"Wskaźnik wygaszania lawy: {wskaznik_wygaszania_lawy}")
    print(f"Prawdopodobieństwo zapłonu od lawy: {p_zaplonu_od_lawy}")
    print(f"Szansa na odrodzenie drzewa: {szansa_na_odrodzenie_drzewa}")
    print(f"Wskaźnik wzrostu rozprzestrzeniania poprzez wiatr: {wskaznik_wzrostu_rozprzestrzeniania}")
    
    # Inicjalizacja siatki
    x = inicjalizacja_gridu(rozmiar_siatki,STANY,proporcje)
    # Wyświetlenie siatki poczatkowej
    #print_grid(x)
    # Rozpoczęcie symulacji
    x = iteracja(x,ilosc_iteracji,rozmiar_siatki,p_zaplonu_od_sasiada,
                 p_samozaplonu,czas_odnowienia_drzewa,WEKTORY_KIERUNKU_WIATRU
                 ,czestotliwosc_zmiany_wiatru,wskaznik_wzrostu_rozprzestrzeniania,wskaznik_erupcji_lawy,
                 wskaznik_rozprzestrzeniania_sadzonek,wskaznik_wygaszania_lawy,p_zaplonu_od_lawy,szansa_na_odrodzenie_drzewa)
    T= konwertuj_macierz_na_obraz(x[len(Holder_grid)-1],obrazki_symulacji,zdjecie_frame)
    dane_z_gridu(x)
    #wykres(Holder_grid[len(Holder_grid)-1])

STANY = [PUSTY,DRZEWO,WODA,PLONACE_DRZEWO,SPALONE_DRZEWO,LAWA]
STANY1 = ["PUSTY","DRZEWO","WODA","PLONACE_DRZEWO","SPALONE_DRZEWO","LAWA"]
def print_grid(grid):
    for row in grid:
        print(" ".join([str(cell) for cell in row]))
def inicjalizacja_gridu(rozmiar_siatki,STANY,proporcje):
    grid = np.random.choice([PUSTY, DRZEWO,WODA,LAWA], 
                            size=(rozmiar_siatki, rozmiar_siatki), 
                            p=[proporcje[0],proporcje[1],proporcje[2],proporcje[3]]) 
    
    return grid
def skanuj_otoczenie(grid,x,y,rozmiar_siatki,prawdopodobienstwo_zaplonu_od_sasiada,wektor_wiatru,wskaznik_wzrostu_rozprzestrzeniania,p_zaplonu_od_lawy):
    x_1 = (x-1)%rozmiar_siatki
    y_1 = (y-1)%rozmiar_siatki
    x1 = (x+1)%rozmiar_siatki
    y1 = (y+1)%rozmiar_siatki

    lista_x = [(x_1 + i) % rozmiar_siatki for i in range((x1 - x_1 + rozmiar_siatki) % rozmiar_siatki + 1)]
    lista_y = [(y_1 + i) % rozmiar_siatki for i in range((y1 - y_1 + rozmiar_siatki) % rozmiar_siatki + 1)]
    tracker_x = [-1,0,1]
    tracker_y = [-1,0,1]

    for i,A in zip(lista_x,tracker_x):
        for j,B in zip(lista_y,tracker_y):
                if grid[i][j] == PLONACE_DRZEWO:
                    if wektor_wiatru[0]+B== 0 and wektor_wiatru[1]+A ==  0:
                        if random.random() < (prawdopodobienstwo_zaplonu_od_sasiada*wskaznik_wzrostu_rozprzestrzeniania):
                            return True
                    else:
                        if random.random() < prawdopodobienstwo_zaplonu_od_sasiada:
                            return True
                if grid[i][j] == LAWA:
                    if(random.random() < p_zaplonu_od_lawy):
                        return True
                

    return False
def skanuj_otoczenie_Puste_Pole(grid,x,y,rozmiar_siatki,wskaznik_rozprzestrzeniania_sadzonek):
    x_1 = (x-1)%rozmiar_siatki
    y_1 = (y-1)%rozmiar_siatki
    x1 = (x+1)%rozmiar_siatki
    y1 = (y+1)%rozmiar_siatki
    counter = 0
    lista_x = [(x_1 + i) % rozmiar_siatki for i in range((x1 - x_1 + rozmiar_siatki) % rozmiar_siatki + 1)]
    lista_y = [(y_1 + i) % rozmiar_siatki for i in range((y1 - y_1 + rozmiar_siatki) % rozmiar_siatki + 1)]
    for i in lista_x:
        for j in lista_y:
            if(grid[i][j]==DRZEWO):
                counter += 1
    if counter >0:
        if random.random() < (wskaznik_rozprzestrzeniania_sadzonek*counter):
            return True
    return False





def iteracja(grid,iteracje,rozmiar_siatki,prawdopodobienstwo_zaplonu_od_sasiada,
             prawdopodobienstwo_samozaplonu,czas_odnowienia_drzewa,wektory_kierunku_wiatru,
             czestotliwosc_zmiany_kierunku_wiatru,wskaznik_wzrostu_rozprzestrzeniania,
             wskaznik_erupcji_lawy,wskaznik_wzrostu_rozprzestrzeniania_sadzonek,wskaźnik_wygaszania_lawy,p_zaplonu_od_lawy,szansa_na_odrodzenie_drzewa):
    # zmienna globalna przechowujaca grid 
    global Holder_grid
    Holder_grid = []
    # Zainicjowanie pozaru w losowym miejscu 
    grid[random.randrange(0,len(grid))][random.randrange(0,len(grid[0]))] = PLONACE_DRZEWO
    # robie kopie gdyz inaczej przypisuje referencje a nie wartosc
    Holder_grid.append(grid.copy())
    # Deklaracja macierzy sluzacej do trackowania zmian w gridzie, 
    # jesli drzewo spalone to dodaj do macierzy,
    # jesli upłynął czas odnowienia to zamien na drzewo lub puste pole i wyzeruj wartosc pola
    macierz_spalonych =  np.zeros((rozmiar_siatki,rozmiar_siatki))
    # Deklaracja macierzy sluzacej do trackowania zmian w gridzie, jesli lawa wygasła to zamien na puste pole, jesli nie to dodaj do macierz
    macierz_Lawy =  np.zeros((rozmiar_siatki,rozmiar_siatki))
    # dodaj lawe inicjacyjna do macierzy sledzenia lawy 
    for i in range(rozmiar_siatki):
        for j in range(rozmiar_siatki):
            if(grid[i][j]==LAWA):
                macierz_Lawy[i][j] = 1 # zainicjowanie lawy 
    flaga_iteracji_wiatru = 0 
    wiatr = zmien_kierunek_wiatru()
    # zmienna globalna przechowujaca kierunek wiatru 
    global Holder_wiatru
    Holder_wiatru = []
    # dodaj kierunek wiatru do listy aby móc go później wyświetlić 
    Holder_wiatru.append(wiatr)
    # grid poczatkowy 
    operowany_grid = None
    # grid tymczasowy, do którego będą wpisywane zmiany
    Nowy_grid = None
    # Flaga do sprawdzania czy na gridzie istnieja plonace drzewa 
    Czy_istnieje_plonace_drzewo = True
    Czy_zainicjowany = False
    
    for p in range(iteracje):
        # jesli na mapie nie ma plonacych drzew, zakoncz symulacje 
        if(Czy_istnieje_plonace_drzewo == False):
            return Holder_grid
        # Zmiana kierunku wiatru
        flaga_iteracji_wiatru += 1
        # zmiana kierunku wiatru co czestotliwosc_zmiany_kierunku_wiatru iteracji 
        if(flaga_iteracji_wiatru == czestotliwosc_zmiany_kierunku_wiatru):
            wiatr = zmien_kierunek_wiatru()
            flaga_iteracji_wiatru = 0
        # jesli grid nie istnieje zainicjuj go tym wygenerwoanym na pooczatku
        if operowany_grid is None:
            operowany_grid = grid.copy()
        # jednak jesli mineła już iteracja to przypisz nowy grid do operowanego
        if(Nowy_grid is not None):
            operowany_grid = Nowy_grid.copy() 
        # dodaj kierunek wiatru do listy 
        Holder_wiatru.append(wiatr)
        # grid tymczasowy, do którego będą wpisywane zmiany
        Nowy_grid = operowany_grid.copy()
        # Erupcja lawy
        for x in range(rozmiar_siatki):
            for y in range(rozmiar_siatki):
                if(operowany_grid[x][y]==PUSTY):
                    if random.random() < wskaznik_erupcji_lawy:
                        Nowy_grid[x][y] = LAWA
        # Iteracja po gridzie 
        for x in range(rozmiar_siatki):
            for y in range(rozmiar_siatki):
                # Jesli woda to pomiń
                if operowany_grid[x][y] == WODA:
                    pass
                # Jesli drzewo płoneło zamien na spalone drzewo
                if operowany_grid[x][y] == PLONACE_DRZEWO:
                    Nowy_grid[x][y] = SPALONE_DRZEWO
                # jesli drzewo jest spalone i upłynął czas odnowienia 
                elif operowany_grid[x][y] == SPALONE_DRZEWO and macierz_spalonych[x][y] >= czas_odnowienia_drzewa: 
                    if(random.random() < szansa_na_odrodzenie_drzewa):
                        Nowy_grid[x][y] = DRZEWO
                    else:
                        Nowy_grid[x][y] = PUSTY
                    macierz_spalonych[x][y] = 0
                # jesli drzewo jest spalone i nie upłynął czas odnowienia dodaj do macierzy spalonych
                elif operowany_grid[x][y] == SPALONE_DRZEWO and macierz_spalonych[x][y] < czas_odnowienia_drzewa:
                    macierz_spalonych[x][y] += 1
                # Sprawdzanie drzewa 
                elif operowany_grid[x][y] == DRZEWO:
                    # Przeszukaj otoczenie drzewa w poszukiwaniu płonących drzew
                    if(random.random() < prawdopodobienstwo_samozaplonu):
                        Nowy_grid[x][y] = PLONACE_DRZEWO
                    elif(skanuj_otoczenie(operowany_grid,x,y,rozmiar_siatki,prawdopodobienstwo_zaplonu_od_sasiada,wiatr,wskaznik_wzrostu_rozprzestrzeniania,p_zaplonu_od_lawy)):
                        Nowy_grid[x][y] = PLONACE_DRZEWO
                # Rozprzestrzenianie sadzonek 
                elif operowany_grid[x][y]==PUSTY:
                    if(skanuj_otoczenie_Puste_Pole(operowany_grid,x,y,rozmiar_siatki,wskaznik_wzrostu_rozprzestrzeniania_sadzonek)):
                        Nowy_grid[x][y] = DRZEWO
                # Rozprzestrzenianie lawy 
                elif operowany_grid[x][y]==LAWA:
                    if(macierz_Lawy[x][y] >= wskaźnik_wygaszania_lawy):
                        Nowy_grid[x][y] = PUSTY
                        macierz_Lawy[x][y] = 0
                    else:
                        macierz_Lawy[x][y] += 1
        # zapisz nowy grid do macierzy sledzenia gridów, aby móc je później wyświetlić
        Holder_grid.append(Nowy_grid.copy()) 
        # Sprawdz czy grid posiada plonace drzewa 
        Czy_istnieje_plonace_drzewo = sprawdz_czy_istnieje_plonace_drzewo(Nowy_grid)
        
    return Holder_grid
# funkcja zmieniająca kierunek wiatru
def sprawdz_czy_istnieje_plonace_drzewo(grid):
    for x in range(len(grid)):
            for y in range(len(grid[0])):
                # sprawdzenie czy pole jest plonacym drzewem 
                if(grid[x][y]==PLONACE_DRZEWO):
                    return True
    return False
def zmien_kierunek_wiatru():
    nowy_kierunek = random.choice(WEKTORY_KIERUNKU_WIATRU)
    return nowy_kierunek
# dodaj przycisk rozpocznij symulacje
Button(frame_parametry, text="Rozpocznij symulacje", command=Symulacja,bg="purple").grid(row=17, column=0, columnspan=2, pady=10)
def zamknij():
    root.destroy()
    sys.exit()
# zamkniecie tk inter i wlaczenie procesu python 
root.protocol("WM_DELETE_WINDOW", zamknij)
root.mainloop()

