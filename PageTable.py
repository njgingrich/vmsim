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
        The page table also needs to store most of the parameter values.
        """
        self.table = {}
        self.cur_frame = 0
        self.pagesize = pagesize
        self.vasize = vasize
        self.ram = ram
        self.algorithm = algorithm
        self.offset_bits = int(math.log(pagesize, 2))

    def create_page(self, page_num, dirty, frame_num):
        """ Put a new page into the page table with the given values. """
        self.table[page_num] = Entry(True, True, dirty, 0b10000000, frame_num)
        return (self.table[page_num], page_num)

    def evict_page(self):
        """
        Remove a page from the table and replace it with a new page.
        For the refhistory algorithm, find the pages with the lowest history.
        Then select the lowest-numbered page from that list of pages.
        The entire list will be replaced if a page with a lower history is found.
        """
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
        """
        Find a frame for the given page. If there is an available frame, increment
        the current frame and return the frame number.
        If there are no frames, evict a page from the frame selected by the eviction
        policy (refhistory) and return the frame number.
        """
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
        """ Get the page number from a virtual address. """
        return va >> self.offset_bits

    def get_offset(self, va):
        """ Get the offset from a virtual address. """
        return int(va % self.ram)

    def get_entry(self, va):
        """
        Get the page table entry for a virtual address.
        Returns a tuple of (entry, page_number)
        """
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
        """ Mark the given page as dirty. """
        self.table[page_num].dirty = True

    def dump(self):
        """ Print out the valid page table entries, and their information. """
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
        """ Update the history bits for each page table entry. """
        for key in self.table:
            self.table[key].ref = False
            self.table[key].history = (self.table[key].history >> 1) | 0b10000000

