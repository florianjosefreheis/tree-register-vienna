import sqlite3
import time
import zlib
import string
import pdb

conn = sqlite3.connect('tree_register_vienna.sqlite')
cur = conn.cursor()

cur.execute('SELECT tree_species FROM Tree WHERE tree_species NOT IN ("Leerer Baumstandort")')

tree_species = dict()
counter = 0
for species in cur :
    tree_species[species[0]] = species[0]
    
cur.execute('SELECT tree_species FROM Tree WHERE tree_species NOT IN ("Leerer Baumstandort")')
counts = dict()
for species in cur :
    text = tree_species[species[0]]
    text = text.replace("'", "")
    text = text.strip()
    text = text.lower()
    if len(text) < 4 : continue
    counts[text] = counts.get(text,0) + 1

x = sorted(counts, key=counts.get, reverse=True)
highest = None
lowest = None
for k in x[:100]:
    if highest is None or highest < counts[k] :
        highest = counts[k]
    if lowest is None or lowest > counts[k] :
        lowest = counts[k]
print('Range of counts:',highest,lowest)

bigsize = 80
smallsize = 20

fhand = open('tree_species_word_clound.js','w')
fhand.write("tree_species_word_clound = [")
first = True
for k in x[:100]:
    if not first : fhand.write( ",\n")
    first = False
    size = counts[k]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")
fhand.close()

print("Output written to tree_species_word_cloud.js.")
print("Open tree_species_word_cloud.htm in a browser to see the vizualization.")
