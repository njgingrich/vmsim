import argparse

"""
This project will simulate a virtual memory system.
It takes a stream of virtual memory references from standard input
and prints the physical addresses associated with those virtual
memory addresses to standard output.

When a page fault occurs, the program chooses the page to be replaced
based on the replacement policy specified in the commandline arguments.

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

def main():
    print "arg parsing"
