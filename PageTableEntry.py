class PageTableEntry:
    def __init__(self, valid, ref, dirty, history, frame):
        self.valid   = valid
        self.ref     = ref
        self.dirty   = dirty
        self.history = history
        self.frame   = frame
