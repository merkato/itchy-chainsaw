#!/usr/bin/python
import csv
import re

r = re.compile("([a-zA-Z]+)([0-9]+)")

new_rows = []

with open('csv/indeks.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        cells = row[3].split(',')
        assoc = {}
        for cell in cells:
            m = r.match(cell)
            if not m:
                row.append('idx_merged')
                pass
            else:
                litera = m.group(1)
                cyfra = m.group(2)
                if litera in assoc.keys():
                    assoc[litera].append(int(cyfra))
                else:
                    assoc[litera] = [int(cyfra)]
        wynik = []
        for k,v in assoc.iteritems():
            if len(v) == 1:
                wynik.append(k+str(v[0]))
            else:
                dol = min(v)
                gora = max(v)
                wynik.append(k+str(dol)+'-'+str(gora))
        row.append(','.join(wynik))
        new_rows.append(row)

with open('csv/index_mod.csv','wb') as newfile:
    writer = csv.writer(newfile, delimiter=';',quotechar='"')
    writer.writerows(new_rows)
