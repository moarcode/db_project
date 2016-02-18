#!/usr/bin/python
__author__ = 'mpacek'

import mysql.connector          # obsluga bazy
import sys                      # obsluga kodow wyjscia programu
import getopt                   # obsluga parametrow
import pygal                    # biblioteka do generowania wykresow
from pygal.style import *       # style wykresow


def available_queries():
    print ("""
             Dostepne zapytania:
                 top-[ip, req, stat]         : Licznik wystapien IP, stron, statusow HTTP
                 byte-req                    : Strony z najwieksza iloscia wyslanych danych
                 byte-perc-[ip, req, stat]   : Procentowy udzial bajow w stosunku do calosci ruchu"""
             )

def usage():
    print ("""
            Skrypt do generowania wykresow na podstawie logow Apache
                -h --help : Pomoc
                -q        : Zapytanie
                -c        : Typ wykresu [pie, pie-hole, half-pie, bar]
                -t        : Limit wynikow
                
                Przykladowe uzycie: ./init.py -q top-ip -c pie -t 10 -o wykres.svg"""
            )
    available_queries()

def cons_dict(q):
    cursor.execute(q)
    dict = {}
    for i in cursor:
        dict[i[0]]=i[1]

    return dict

def get_query(top_num, v, q):
    return cons_dict(q % (v, top_num))

def get_query_1arg(top_num, q):
    return cons_dict(q % top_num)

# Generowanie wykresu
def gen_chart(dict, title, output, chart):

    # Wykres kolowy
    if chart == "pie":
        _chart = pygal.Pie(style=NeonStyle)
    # Wykres typu paczek :)
    if chart == "pie-hole":
        _chart = pygal.Pie(inner_radius=.4, style=DarkColorizedStyle)
    # Pol ciasktka :)
    if chart == "half-pie":
        _chart = pygal.Pie(half_pie=True, style=TurquoiseStyle)
    # Wykres slupkowy
    elif chart == "bar":
        _chart = pygal.Bar(style=DarkGreenStyle)
    for i in dict.iteritems():
        _chart.add(i[0], i[1])
    _chart.title=title

    # Sciezka do zapisu pliku
    _chart.render_to_file('/var/www/%s' % output)


# Polaczenie z baza
cnx = mysql.connector.connect(user='root', password='deska21',
                              host='127.0.0.1',
                              database='apache_logs')
cursor = cnx.cursor()


queries = {
	"bytes_perc":
		"""select %s as f, sum(int_bytes) / (select sum(int_bytes) from apache_log2) * 100 
		as t from apache_log2 group by f order by t desc limit %s""",
	"bytes_perc_by_host": 
		"""select if (CHAR_LENGTH(var_request) > 20, CONCAT(LEFT(var_request, 20), '...'), 
		var_request), sum(int_bytes) as sum from apache_log2  group by var_request order by 
		sum desc limit %s;""",
	"top": 
		"""select %s as f, sum(int_bytes) / (select sum(int_bytes) from apache_log2) * 100 
		as t from apache_log2 group by f order by t desc limit %s"""
	}

chart_param = {
	"byte-perc-ip":['var_host', "Bytes per IP according to all bytes requested [%]", queries["bytes_perc"]], 
	"byte-perc-req":["var_request","Bytes requestes for site / all bytes [%]", queries["bytes_perc"]],
	"byte-perc-stat":["var_request", "Bytes requestes in comparation to HTTP responses", queries["bytes_perc"]],
	"top-req":["var_request", "Top sites requested", queries["top"]],
	"top-ip":["var_host", "Top IPs connected to the server", queries["top"]],
	"top-stat":["enu_http_status", "Top HTTP responses", queries["top"]],
	"byte-req":["var_request", "Bytes count per site", queries["bytes_perc_by_host"]]
	}


# Glowna funkcja programu
if __name__ == "__main__":

    # Odczyt argumentow z linii polecen
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hq:t:c:o:")
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    if opts:
        for opt, arg in opts:                
	    if opt in ("-h", "--help"):      # pomoc
	        usage()                     
	        sys.exit()                  
	    elif opt == '-q':                # typ zapytania
	        query = arg
	    elif opt == '-t':                # limit wynikow
	        top_num = arg
	    elif opt == '-c':                # typ wykresu
	        chart = arg
	    elif opt == '-o':                # plik wyjsciowy
	        output = arg
    else:
        usage()
        sys.exit(2)

    # Generowanie wykresu
    if query == "byte-req":
        gen_chart(get_query_1arg(top_num, chart_param[query][2]), str(chart_param[query][1]), output, chart)
    else:
        gen_chart(get_query(top_num, chart_param[query][0], chart_param[query][2]), str(chart_param[query][1]), output, chart)
	    
    cursor.close()
    cnx.close()
    sys.exit(0)
