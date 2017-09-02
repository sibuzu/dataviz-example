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

cols = sorted(nobel_winners[0].keys())

with open('nobel_winners.csv', 'w') as f:
    f.write(','.join(cols) + '\n')

    for o in nobel_winners:
        row = [str(o[col]) for col in cols]
        f.write(','.join(row) + '\n')
