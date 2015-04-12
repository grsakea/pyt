
class Tweet():
    def __init__(self, status):
        self.status = status
        self.tid = status.id
        self.read = False
