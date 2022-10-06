class Data:
    def __init__(self, feedR, usgR, feedA, usgA):
        self.feedR = feedR
        self.usgR = usgR
        self.feedA = feedA
        self.usgA = usgA

    # Getter feedR
    def get_feedR(self):
        return self.feedR

    # Getter usgR
    def get_usgR(self):
        return self.usgR

    # Getter feedA
    def get_feedA(self):
        return self.feedA

    # Getter usgA
    def get_usgA(self):
        return self.usgA

    # To string
    def __str__(self):
        return "Data(feedR={},usgR={},feedA={},usgA={})".format(
            self.feedR, self.usgR, self.feedA, self.usgA
        )
