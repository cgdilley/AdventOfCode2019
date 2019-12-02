import math

with open("input/input01.txt", "r") as f:
    print(sum([math.floor(int(m.strip())/3) - 2 for m in f.readlines()]))
