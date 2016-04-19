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
        self.table[page_num] = Entry(True, False, dirty, 0b10000000, frame_num)
        return self.table[page_num]

    def find_frame(self):
        self.cur_frame += 1
        return (self.cur_frame - 1)

    def get_page_number(self, va):
        return va >> self.offset_bits

    def get_offset(self, va):
        return int(va % self.ram)

    def get_entry(self, va):
        page_num = self.get_page_number(va)
        try:
            entry = self.table[page_num]
            return entry
        except KeyError:
            print("Page fault for page", page_num)
            frame_num = self.find_frame()
            print("Frame", frame_num, "available, allocated to page", page_num)
            return self.create_page(page_num, False, frame_num)

    def dump(self):
        print("Page #", "Valid", "Ref", "Dirty", "History", "Frame", sep="\t")
        for page in self.table:
            print(page, self.table[page].valid, self.table[page].ref,
                    self.table[page].dirty, str(bin(self.table[page].history))[2:],
                        self.table[page].frame, sep="\t")


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
