import random

ram = 4096
pagesize = 4096
to_gen = 20

while to_gen > 0:
    print("r:", random.randint(0, 100000), sep="")
    if ((to_gen % 10) == 0):
        print("dump")
    to_gen -= 1