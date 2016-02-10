# Program Log_stat 

Program generujacy statystki dla access.log Apache2 pobierajacy dane z bazy MySQL.
Umozliwia generowanie roznych typow wykresow m.in. dla liczy zapytan do serwera WWW z podzialem na IP,
kody odpowiedzi HTTP, przeslanych bajtow oraz procentowego stosunku do calego ruchu WWW.

## Dodatkowe informacje
Przedstawione przykladowe wykresy pochodza z bazy danych stworzonej na podstawie logow z jednego dnia.
Import logow do bazy MySQL wykonalem poprzez plik csv sworzony autorskim skryptem wykorzystujac narzedzia 
do pracy z tekstem dostepne w systemie GNU/Linux m.in. cat, awk, grep, paste.
### Napotkane problemy
Podczas importu bazy danych z pliku csv zauwazylem, ze dane dot. czasu i daty nie zostaly poprawnie zapisane.
Nie moglem sobie poradzic z ta kwestia w sensownym czasie.

## Struktura bazy danych
```
+-----------------+---------------------+------------------------------------------------------------+-----------------+-----------+--------+
| var_host        | tms_stamp           | var_request                                                | enu_http_status | int_bytes | int_id |
+-----------------+---------------------+------------------------------------------------------------+-----------------+-----------+--------+
| 31.184.238.174  | 0000-00-00 00:00:00 | http://buyrepaglinide2mgonline.tumblr.com                  | 200             |   5356590 |      1 |
| 77.37.240.57    | 0000-00-00 00:00:00 | http://inima.ru/contacts/                                  | 200             |   5356590 |      2 |
| 212.92.232.129  | 0000-00-00 00:00:00 | http://omnicef.soup.io/                                    | 404             |        73 |      3 |
| 192.187.100.154 | 0000-00-00 00:00:00 | http://redlug.com/                                         | 200             |       384 |      4 |
| 5.189.177.15    | 0000-00-00 00:00:00 | http://redlug.com/                                         | 200             |       438 |      5 |
| 89.19.178.131   | 0000-00-00 00:00:00 | http://www.xolodremont.ru/remont_holodilnikov_na_domu.html | 200             |      9589 |      6 |
| 89.19.178.131   | 0000-00-00 00:00:00 | http://www.xolodremont.ru/remont_holodilnikov_na_domu.html | 200             |      9589 |      7 |
| 141.8.143.205   | 0000-00-00 00:00:00 | -                                                          | 200             |     15318 |      8 |
| 31.184.238.174  | 0000-00-00 00:00:00 | http://griseofulvinp4.forumcircle.com                      | 200             |      1835 |      9 |
| 31.184.238.174  | 0000-00-00 00:00:00 | http://gravatar.com/floxin7j                               | 200             |      2045 |     10 |
+-----------------+---------------------+------------------------------------------------------------+-----------------+-----------+--------+
```

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

[site]: https://github.com/moarcode/db_project/blob/master/site.svg
