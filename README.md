# Program Log_stat 

Program generujacy statystki dla access.log Apache2 pobierajacy dane z bazy MySQL.
Umozliwia generowanie roznych typow wykresow m.in. dla liczy zapytan do serwera WWW z podzialem na IP,
kody odpowiedzi HTTP, przeslanych bajtow oraz procentowego stosunku do calego ruchu WWW.

## Dodatkowe informacje
Przedstawione przykladowe wykresy pochodza z bazy danych stworzonej na podstawie logow z jednego dnia.
Import logow do bazy MySQL wykonalem autorskim skryptem wykorzystujac narzedzia do pracy z tekstem
dostepne w systemie GNU/Linux m.in. cat, awk, grep, paste.

## Praca z programem
Program obslugiwany jest z linii polecen, sterowanie odbywa sie
poprzez przelaczniki oraz ich argumenty.
Opis poszczegolnych przelacznikow:
```
            Skrypt do generowania wykresow na podstawie logow Apache
                -h --help : Pomoc
                -q        : Zapytanie
                -c        : Typ wykresu [pie, pie-hole, half-pie, bar]
                -t        : Limit wynikow
                
                Przykladowe uzycie: ./log_stat.py -q top-ip -c pie -t 10 -o wykres.svg

             Dostepne zapytania:
                 top-[ip, req, stat]         : Licznik wystapien IP, stron, statusow HTTP
                 byte-req                    : Strony z najwieksza iloscia wyslanych danych
                 byte-perc-[ip, req, stat]   : Procentowy udzial bajow w stosunku do calosci ruchu
```
## Przykladowe uzycie:

./log_stat.py -q top-ip -c bar -t 10 -o test.svg

oznacza wygenerowanie wykresu typu top-ip z limitem 10 pozycji typem wykresu 'bar' do pliku o nazwie test.svg.

Sciezka zapisu plikow jest zapisana na stale: /var/www.
