"""
Page Table Entry Diagram
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
        pass

    def add_page(page_num):
        self.table.insert(page_num, 0x00000000)
        pass

    def replace_page(page_num):
        pass

    def dump():
        pass

