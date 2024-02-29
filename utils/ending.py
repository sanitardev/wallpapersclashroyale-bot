ending = lambda one, two, many, num: (one if (abs(num) % 10 == 1 and abs(num) % 100 != 11) else (two if (1 < abs(num) % 10 < 5 and not (11 < abs(num) % 100 < 15)) else many))
