import sqlite3
import json
import codecs

conn = sqlite3.connect('tree_register_vienna.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Tree')
fhand = codecs.open('tree_locations.js', 'w', "utf-8")
fhand.write("tree_locations = [\n")
count = 0

for row in cur :
    latitude = row[3]
    longitude = row[2]
    
    if latitude == 0 or longitude == 0 : continue
    
    location = row[5]
    
    try :
        count = count + 1
        print(count, location, latitude, longitude)

        if count > 1 : fhand.write(",\n")
        output = "["+str(latitude)+","+str(longitude)+", '"+location+"']"
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print(count, "tree locations written to tree_locations.js.")
print("Open index.html to view the data in a browser.")

