
class Tweet():
    def __init__(self, status):
        self.status = status
        self.tid = status.id

    def __lt__(self, other):
        return self.tid < other.tid
