class Point:
    def __init__(self, x, y, edu=None, payload=None):
        self.x = x
        self.y = y
        self.education = edu
        self.payload = payload

    def __getitem__(self, index):
        if index: return self.y
        else: return self.x
  
        
    def __repr__(self):
        return f'{self.x, self.y}: {repr(self.payload)}'


    def __str__(self):
        return f'({self.x}, {self.y})'