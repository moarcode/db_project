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
    -c        : Typ wykresu (pie, bar)
    """)

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

    cursor.close()
    cnx.close()
    return dict

# Obsluga zapytan TOP 
def top_visited(top_num):
    query = ("""select var_host, count(var_host) 
            from apache_log2 group by var_host 
            order by count(var_host) desc limit %s""" 
            % top_num
            )
    return cons_dict(query)

def top_stat(top_num):
    query = ("""select enu_http_status, count(*) as count 
            from apache_log2 group by enu_http_status 
            order by count desc limit %s """ % top_num
            )
    return cons_dict(query)

def top_stat_by_ip(top_num):
    query = (""" select var_host, count(*) as count 
            from apache_log2 group by var_host order by count 
            desc limit %s """ % top_num
            )
    return cons_dict(query)

def top_bytes_per_site(top_num):
    query = (""" select if (CHAR_LENGTH(var_request) > 20, 
            CONCAT(LEFT(var_request, 20), '...'), var_request), 
            sum(int_bytes) as sum from apache_log2  group by var_request 
            order by sum desc limit %s;""" % top_num
            )
    return cons_dict(query)

def perc_bytes_per_ip(top_num):
    query = (""" select var_host, sum(int_bytes) / (select sum(int_bytes) 
                from apache_log2) * 100 as t from apache_log2 group by var_host 
                order by t desc limit %s""" % top_num
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

    gen_chart(perc_bytes_per_ip(top_num), "Top bytes per site" ,output, chart)
