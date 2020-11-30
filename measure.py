class Measure:
    def __init__(self, low, high, low_to_high=True, cur_list=[4,20]):
        x, y = cur_list
        if low_to_high:            
            self.cur_list = [*range(x, y+1, 4)]
        else:
            self.cur_list = [*range(y, x-1, -4)]
        
        self.low = low
        self.high = high
        self.span = max(low, high) - min(low, high)
        self.step = self.span / 4
        self.pressures = []
        self.set_pressures()
        self.results = {}
        
    
    def set_pressures(self):
        if (self.low<self.high):
            count = self.low
            for i in range(5):
                self.pressures.append(count)
                count += self.step    
        else:
            count = self.high
            for i in range(5):
                self.pressures.append(count)
                count -= self.step
    