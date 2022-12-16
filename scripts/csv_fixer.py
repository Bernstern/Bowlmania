# Fixes some weirdness with the CSV files that are downloaded from the
# scraper where the team name isn't quoted causing pandas to flip

conent = []

target = input("Enter the file name: ")

with open(target, 'r') as f:
    reader = f.readlines()
    for row in reader:
        # Prepend a quote to the row
        row = '"' + row

        # Put a quote before the first comma
        row = row.replace(',', '",', 1)

        conent.append(row)

with open(target, 'w') as f:
    f.write("".join(conent))

