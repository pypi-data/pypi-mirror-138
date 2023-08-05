class Calculator():
    def __init__(self, total = 0 ) -> None:
        self.total = total

    def __str__(self):
        return str(self.total)

    def add(self, x):
        self.total = self.total + x
        return 

    def sub(self, x):
        self.total = self.total - x
        return 
    def mul(self, x):
        self.total = self.total * x
        return 
    def div(self, x):
        self.total = self.total / x
        return 
