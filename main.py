import argparse
import sys

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

# Setup
debug = False

def initialize_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pagesize",  help="the size of pages & frames (in KB)",
                        type=int, required=True)
    parser.add_argument("--vasize",    help="the size of a virtual address (in bits)",
                        type=int, required=True)
    parser.add_argument("--pasize",    help="the size of a physical address (in bits)",
                        type=int, required=True)
    parser.add_argument("--RAM",       help="the size of system memory (in MB)",
                        type=int, required=True)
    parser.add_argument("--algorithm", help="the page replacement policy to use",
                        choices=['clock', 'refhistory'], required=True)
    parser.add_argument("--refhistory-update", help="the length of period between reference history updates",
                        type=int, default=5)
    parser.add_argument("--debug", help="add additional diagnostic information",
                        action="store_true")
    args = parser.parse_args()
    if (args.pasize < args.vasize):
        parser.error("pasize must be at least as large as vasize.")
    if (args.RAM % args.pasize != 0):
        parser.error("RAM must be divisible by pasize.")
    return args

def get_frame_number(addr):
    # frame number is bits 0-15 (rightmost 16 bits)
    if debug:
        print("addr:", addr, "- frame:", addr & 0xff)
    return addr & 0xff

def main():
    args = initialize_args()
    if args.debug:
        global debug
        debug = True
        print(args)

    for line in sys.stdin:
        print(line.rstrip('\n'))
        split = line.split(':')
        get_frame_number(int(split[1].rstrip('\n')))
    print("arg parsing")

main()
