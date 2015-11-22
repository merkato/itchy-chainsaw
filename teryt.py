#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
from slowniki import *

new_rows = []

def contains(list1,list2):
	for i in list1:
		if i in list2:
			return True
	return False

# otwieramy plik
with open('csv/index_mod.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
# rozbijamy na komórki, liczone od zera, gdzie jest name
# Wersja z solectawami: index_mod -> nazwa, solectwo, gmina, idx_f, idx_mod
        cells = row[0].split(',')
        for cell in cells:
			if cell in wyjatki:
				new_rows.append([cell,None,None,row[1],row[2],row[4]])
			else:
				slowo = cell.split()
				nowe_slowo = {'prefixes': [], 'imiona': [], 'nazwiska': [], 'solectwo': row[1], 'gmina': row[2], 'idx_f': row[4]}
				#if contains(prefix, slowo):
				for slowo_f in slowo:
					if contains(prefix,slowo_f):
						nowe_slowo['prefixes'].append(slowo_f)
					elif contains(first_name,slowo_f):
						nowe_slowo['imiona'].append(slowo_f)
					else:
						nowe_slowo['nazwiska'].append(slowo_f)
				matol = [' '.join(nowe_slowo['nazwiska']), ' '.join(nowe_slowo['imiona']), ' '.join(nowe_slowo['prefixes']), ''.join(nowe_slowo['solectwo']), ''.join(nowe_slowo['gmina']), nowe_slowo['idx_f']]
				new_rows.append(matol)
# no i zapisujemy
with open('csv/index_slownikowy.csv','wb') as newfile:
    writer = csv.writer(newfile, delimiter=';',quotechar='"')
    writer.writerows(new_rows)
