import math
import random

ram = 4096
vasize = 16
pagesize = 4096
to_gen = 20

while to_gen > 0:
    max_pages = math.pow(2, vasize-int(math.log(pagesize, 2)))
    max_val = math.pow(2, vasize)
    print(("r" if random.randint(0, 2) == 0 else "w"), ":", random.randint(0, max_val), sep="")
    if ((to_gen % 2) == 0):
        print("dump")
    to_gen -= 1
