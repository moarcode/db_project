#!/usr/bin/python
__author__ = 'mpacek'

import mysql.connector
import datetime
import pygal
import sys
import getopt


def usage():
    print ("""
    -h --help : Pomoc
    -q        : Wykonaj query top_ip, http_stat, http_stat_by_ip
    -c        : Typ wykresu (pie, bar)"""
    )

def available_queries():
    print ("""Dostepne zapytania:
             top-[ip, req, stat]         : Licznik wystapien IP, stron, statusow HTTP
             byte-req                    : Strony z najwieksza iloscia wyslanych danych
             byte-perc-[ip, req, stat]   : Procentowy udzial bajow w stosunku do calosci ruchu"""
             )

# Odczyt argumentow z linii polecen

# Polaczenie z baza
cnx = mysql.connector.connect(user='root', password='deska21',
                              host='127.0.0.1',
                              database='apache_logs')
cursor = cnx.cursor()

def cons_dict(q):
    cursor.execute(q)
    dict = {}
    for i in cursor:
        dict[i[0]]=i[1]

    return dict

# Zliczenie wystapien (var_host, var_request, enu_http_status)
def top_count(top_num, v):
    query = (""" select %s as f, count(*) as c
            from apache_log2 group by f 
            order by c desc limit %s""" 
            % (v, top_num)
            )
    return cons_dict(query)

# Zliczenie bajtow dla requestow z ucieciem adresow dluzych niz 20 znakow
def top_bytes_per_site(top_num):
    query = (""" select if (CHAR_LENGTH(var_request) > 20, 
            CONCAT(LEFT(var_request, 20), '...'), var_request), 
            sum(int_bytes) as sum from apache_log2  group by var_request 
            order by sum desc limit %s;""" % top_num
            )
    return cons_dict(query)

# Procentowy udzial bajtow zgrupowany po :(var_host, var_request, enu_http_status)
def perc_bytes_per_var(top_num, v):
    query = (""" select %s as f, sum(int_bytes) / (select sum(int_bytes) 
                from apache_log2) * 100 as t from apache_log2 group by f
                order by t desc limit %s""" % (v, top_num)
                )
    return cons_dict(query)

# Generowanie wykresu
def gen_chart(dict, title, output, chart):

    if chart == "pie":
        _chart = pygal.Pie()
    elif chart == "bar":
        _chart = pygal.Bar()
    for i in dict.iteritems():
        _chart.add(i[0], i[1])
    _chart.title=title

    # Sciezka do zapisu pliku
    _chart.render_to_file('/var/www/%s' % output)



if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hq:t:c:o:")
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    if opts:
        for opt, arg in opts:                #(2)
            if opt in ("-h", "--help"):      #(3)
                usage()                     
                sys.exit()                  
            elif opt == '-q':                #(4)
                query = arg
            elif opt == '-t':                #(4)
                top_num = arg
            elif opt == '-c':                #(4)
                chart = arg
            elif opt == '-o':                #(4)
                output = arg
    else:
        usage()
        sys.exit(2)

    #gen_chart(perc_bytes_per_var(top_num, "enu_http_status"), "Top bytes per site" ,output, chart)

    if query == "top-ip":
        gen_chart(top_count(top_num, "var_host"), "Top IPs conneced to server", output, chart)
    elif query == "top-req":
        gen_chart(top_count(top_num, "var_request"), "Top sites requested", output, chart)
    elif query == "top-stat":
        gen_chart(top_count(top_num, "enu_http_status"), "Top HTTP responses", output, chart)
    elif query == "byte-req":
        gen_chart(top_bytes_per_site(top_num, "var_request"), "Bytes count per site", output, chart)
    elif query == "byte-perc-ip":
        gen_chart(perc_bytes_per_var(top_num, "var_host"), "Bytes per IP according to all bytes requested [%]", output, chart)
    elif query == "byte-perc-req":
        gen_chart(perc_bytes_per_var(top_num, "var_request"), "Bytes requestes for site / all bytes [%]", output, chart)
    elif query == "byte-perc-stat":
        gen_chart(perc_bytes_per_var(top_num, "var_request"), "Bytes requestes in comparation to HTTP responses", output, chart)
    else:
        print "Please select proper query"
        available_queries()

    cursor.close()
    cnx.close()