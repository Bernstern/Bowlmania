# Load up data/cfb21.csv
import csv
conent = []

with open('data/cfb21.csv', 'r') as f:
    reader = f.readlines()
    for row in reader:
        # Prepend a quote to the row
        row = '"' + row

        # Put a quote before the first comma
        row = row.replace(',', '",', 1)

        conent.append(row)
print(conent)
with open('data/cfb21.csv', 'w') as f:
    f.write("".join(conent))

