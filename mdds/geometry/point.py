class Point:
    def __init__(self, x, y, payload=None, id=None):
        self.x = x
        self.y = y
        self.payload = payload
        self.id = id

    def __getitem__(self, index):
        if index: return self.y
        else: return self.x
  
        
    def __repr__(self):
        return f'{self.x, self.y}: {repr(self.id)}'


    def __str__(self):
        return f'({self.x}, {self.y})'