'''
Created on 15 Nov 2015

@author: Allan
'''
class trad(object):
    i =None
    

class aStock(object):
    '''
    The place to create and hold individual stocks
    '''
    symbol = None       # What to call it
    type = None         # What is it
    lastDividend = None # The last dividend
    fixedDividend = None    # For preferred stock
    parValue = None         # Current par value
    

    def __init__(self, symbol, type, parval=None, dividend=None,fdividenbd=None ):
        '''
        Symbol and type are not optional
        The rest are optional
        '''
        self.symbol = symbol
        self.type = type
        self.parValue = parval
        self.lastDividend = dividend
        self.fixedDividend = fdividenbd
        

if __name__ == '__main__':
    pass