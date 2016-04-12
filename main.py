import argparse

"""
This project will simulate a virtual memory system.
It takes a stream of virtual memory references from standard input
and prints the physical addresses associated with those virtual
memory addresses to standard output.

When a page fault occurs, the program chooses the page to be replaced
based on the replacement policy specified in the commandline arguments.

Each memory reference will be in the format op:address. 'op' will be either
'r' or 'w', for read/write.
Each page table entry is 4 bytes, with the frame number in the 2 lower bytes.
Not all 16 bits may be needed, but are reserved - little endian is used.
PTE:
    bits  0-15: frame number
    bits 16-23: stores page reference history (most recent in bit 23)
    bit     24: valid
    bit     25: reference
    bit     26: modified
    bits 27-31: reserved

Frames will be used in numerical order. Once a frame is allocated to a process,
it is never deallocated.

Arguments:
    --pagesize:  the size of pages/frames (in KB)
    --vasize:    size of a virtual address (in bits)
    --pasize:    size of a physical address (in bits). Must be >= vasize.
    --RAM:       the size of the system's memory (in MB). Must be divisible
                 by pagesize, and cannot be too large for value of pasize.
    --algorithm: the page replacement policy to be used (clock or refhistory).
Optional Arguments:
    --refhistory-update: specifies length of period between updates of each page's
                         reference history word (ex: 10 -> updates on 10th, 20th,
                         memory reference). Defaults to 5.
    --debug:             program will print out additional diagnostic information.
                         Defaults to False.
"""

def initialize_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("pagesize",  help="the size of pages & frames (in KB)")
    parser.add_argument("vasize",    help="the size of a virtual address (in bits)")
    parser.add_argument("pasize",    help="the size of a physical address (in bits)")
    parser.add_argument("RAM",       help="the size of system memory (in MB)")
    parser.add_argument("algorithm", help="the page replacement policy to use")

def main():
    initialize_args()
    print("arg parsing")
