'''
...
'''

try:
    from datetime import datetime
except: 
    print("This module needs the following packages: datetime")
    exit(1)

class Cache:
    '''
    ...
    '''

    def __init__(self, type):
        self.cached = []
        self.type = type

    def add(self, item):
        '''
        ...
        '''
        if isinstance(item, self.type): 
            self.cached.append([item, datetime.now()])
            return len(self.cached)-1
        elif isinstance(item, list):
            [self.cached.append([x, datetime.now()]) for x in item]
        else: raise Exception("Another type of data.")
    
    def get(self, index):
        '''
        ...
        '''
        return self.cached[index][0]

    def clear(self, date:datetime):
        '''
        ...
        '''
        i = len(self.cached)-1
        while True: 
            if self.cached[i][1] <= date: 
                del self.cached[i]
            else: break

            if i >= 1: i -= 1
            else:break