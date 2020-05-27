import sys
import os
import re
from numpy import uint, dtype
from PIL import Image

mas = [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4],]
a = range(-2, 3)
print(a)
for i in a:
    for j in a:
        if i + 2 > -1 :
            if j + 2 > -1 :
                print(i, end=' ')
            else:
                print('None', end=' ')
        else:
            print('None', end=' ')
    print()

print(len(mas[1]))

