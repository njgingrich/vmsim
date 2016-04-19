import math
from PageTableEntry import PageTableEntry as Entry

"""
Page Table Entry Diagram
10987654 32109876 54321098 76543210
33222222 22222111 11111110 00000000
________ ________ ________ ________
|   |||| |      | |               |
|   |||| |      | +---------------+-- frame number
|   |||| +------+-- reference history
|   |||+-- valid bit
|   ||+-- reference bit
|   |+-- modified bit
+---+-- reserved

"""

class PageTable:
    def __init__(self, pagesize, vasize, ram, algorithm):
        """
        Each entry in the table is a PageTableEntry.
        """
        self.table = {}
        self.cur_frame = 0
        self.pagesize = pagesize
        self.vasize = vasize
        self.ram = ram
        self.algorithm = algorithm
        self.offset_bits = int(math.log(pagesize, 2))

    def create_page(self, page_num, dirty, frame_num):
        self.table[page_num] = Entry(True, True, dirty, 0b10000000, frame_num)
        return (self.table[page_num], page_num)

    def evict_page(self):
        least_history = 0b11111111
        history_list = []
        for key in sorted(self.table):
            if self.table[key].history < least_history:
                least_history = self.table[key].history
                history_list = [(key, self.table[key])]
            elif self.table[key].history == least_history:
                history_list.append((key, self.table[key]))

        return history_list[0]

    def find_frame(self, page_num):
        #max_frames = self.ram/self.pagesize
        max_frames = 4

        if self.cur_frame == max_frames:
            # need to evict a page, find one with least refhistory
            # get list of ones with lowest refhistory - select lowest # from those
            print("No frames available; choosing victim")
            (key, entry) = self.evict_page()
            print("Page", key, "chosen as victim, located in frame", entry.frame)
            del self.table[key]
            return entry.frame
        else:
            self.cur_frame += 1
            print("Frame", (self.cur_frame-1), "available, allocated to page", page_num)
            return (self.cur_frame - 1)

    def get_page_number(self, va):
        return va >> self.offset_bits

    def get_offset(self, va):
        return int(va % self.ram)

    def get_entry(self, va):
        page_num = self.get_page_number(va)
        print("Page: ", page_num, ",", " offset ", self.get_offset(va), sep="")
        try:
            entry = self.table[page_num]
            print("Valid entry, stored in frame", entry.frame)
            # set ref bit to true
            self.table[page_num].ref = True
            return (entry, page_num)
        except KeyError:
            print("Page fault for page", page_num)
            frame_num = self.find_frame(page_num)
            return self.create_page(page_num, False, frame_num)

    def write_page(self, page_num):
        self.table[page_num].dirty = True

    def dump(self):
        print("Page #", "Valid", "Ref.", "Dirty", "History\t", "Frame", sep="\t")
        for page in sorted(self.table):
            print(page,
                  ("Yes" if self.table[page].valid else "No"),
                  ("Yes" if self.table[page].ref else "No"),
                  ("Yes" if self.table[page].dirty else "No"),
                  str(bin(self.table[page].history))[2:],
                  self.table[page].frame,
                  sep="\t")

    def update_refhistory(self):
        for key in self.table:
            self.table[key].ref = False
            self.table[key].history = (self.table[key].history >> 1) | 0b10000000

"""
Determine the physical address from a virtual address:
    1) get the number of bits required for the offset -> offset_bits = log(2, pagesize)
    2) get the page number                            -> v_addr >> offset_bits
    3) get the offset                                 -> v_addr % ram
    4) see if page is in table
    4.1) if yes, return physical address
    4.2) if no, find an open frame and allocate it to that page
    4.2.1) if no frames available, evict as necessary ***
    4.3) the physical address will be                 -> frame_num * pagesize + offset
"""
