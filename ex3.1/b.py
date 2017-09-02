import csv

nobel_winners = [
    {'catalog': 'Physics',
     'name': 'Albert Einstein',
     'nationality': 'Swiss',
     'sex': 'male',
     'year': 1921},
    {'catalog': 'Physics',
     'name': 'Paul Dirac',
     'nationality': 'British',
     'sex': 'male',
     'year': 1933},
    {'catalog': 'Chemistry',
     'name': 'Marie Curie',
     'nationality': 'Polish',
     'sex': 'female',
     'year': 1911},
]

with open('nobel_winner2.csv', 'w') as f:
    cols = sorted(nobel_winners[0].keys())
    writer = csv.DictWriter(f, fieldnames=cols)
    writer.writeheader()
    for w in nobel_winners:
        writer.writerow(w)
