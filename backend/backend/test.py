import numpy as np

m = np.matrix([
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 1, 0, 1],
    [0, 1, 0, 1, 0]
])

m

with open('MovieGenre-1.csv','r') as reader:
    for line in reader:
        fields = line.split(',')
        print(fields[5])