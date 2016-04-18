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
    def __init__(self):
        # The page table is an array with a 32-bit value in each index
        # The index of the array is the page number.
        self.table = []
        self.cur_frame = 0
        pass

    def find_open_frame(self):
        ret = self.cur_frame
        self.cur_frame += 1
        return ret

    def add_entry(addr):
        page_num = int(pagesize/addr)

    def add_page(self, page_num, va):
        # an entry won't be added to page table until it's valid, so
        # ref bit will be initially set to 1

        pte = 0x00000000
        self.table.insert(page_num, 0x00000000)
        # init refhistory to 1000000, valid bit to 1,
        # ref bit to 1, modified bit to 0
        # 0xfbf80ffff = 11111011 10000000 11111111 11111111
        pte = pte & 0xfbf80ffff

        # init frame number
        frame = self.find_open_frame()
        # mask with 11111111 11111111 00000000 00000000
        pte = (pte & 0xffff0000) + frame

    def replace_page(self, page_num):
        pass

    def dump(self):
        print("Page #", "Valid", "Ref", "Dirty", "History", "Frame", sep="\t")
        for (ix, entry) in enumerate(self.table):
            print(ix, ix&0x1000000, ix&0x2000000, ix&0x4000000, ix&0xff0000, ix&0xffff, sep="\t")
        pass












