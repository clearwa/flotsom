'''
Created on 15 Nov 2015

@author: Allan Clearwaters

Super Simple Stocks
'''
from datetime import *
import datetime
from scipy.cluster.hierarchy import dendrogram
import math

#Transaction types
BUY = True
SELL = False

#Types of stock
COMMON = False
PREF = True

class trade(object):
    ''' The default trade is BUY, hos all attributes as 0, and the date is the
    beginning of the epoch
    '''
    price = float(0)
    quantity = 0
    dtme = datetime.datetime(1, 1, 1)
    ttype = BUY     # True => buy, False => sell
    
    def __init__(self, quant, price, dtme, ttype):
        self.price = float(price)
        self.quantity = quant
        # Make sure the date tag is in the right format
        self.dtme = dtme
        self.type = ttype
        
class aStock(object):
    '''
    The class for individual stocks
    Common stoack are always valid, Preferred stock is valid
    only if the fixed dividend != None
    '''
    symbol = ''       # What to call it
    pref = COMMON         # What is it
    lastDividend = float(0)     # The last dividend
    __fixedDividend = None    # For preferred stock
    parValue = float(0)        # Current par value
    __valid = True
    trades = None             #List of trades
    
    def __setFixedDividend(self, fdividend ):
        '''  Check the consistency of a preferred stock
        '''
        #Consistancy check
        if fdividend != None:
            self.__fixedDividend = float(fdividend)      
        elif self.pref == PREF:  
            print ("Preferred stock must have a fixed dividend")
            self.__valid = False

    def __init__(self, symb, pref=COMMON, parval=0, dividend=0,fdividend=None ):
        '''
        Symbol and type are not optional
        The rest are optional
        '''
        self.symbol = symb
        self.parValue = float(parval)
        self.lastDividend = float(dividend)
        self.preferred = pref
        self.__setFixedDividend( fdividend )
    
    def recordTrade(self, quant, price, date, ttype ):
        ''' Append a trade to the trades list
        '''
        if self.trades == None:
            # Lazy initialization
            self.trades =[]
        
        self.trades.append( trade( quant, price, date, ttype) )

    def currentYield(self, tickerPrice ):
        ''' Calculate the yield
        '''
        ret = None
        if self.__valid:
            ret = ((self.__fixedDividend*self.parValue)/tickerPrice) if (self.__valid) else (self.lastDividend/tickerPrice)
        return float(ret)
    
    def peRatio(self, tickerPrice ):
        ''' Calculate the pe ratio
        '''
        return tickerPrice/self.lastDividend
    
    def stockPrice(self):
        '''  Calculate the price. Return None if there are no trades
        '''
        acount = 0.0
        asum = 0.0
        
        # What is the date range
        dtend = datetime.datetime.now()
        dwindow = datetime.timedelta(minutes=15)
        
        if self.trades == None:
            return None
        
        for thistrade in self.trades:
            if (dtend - thistrade.dtme) < dwindow:
                asum += thistrade.price * thistrade.quantity
                acount += thistrade.quantity
        return float(asum/acount)
    
def allShareIndex( allshares ):
    ''' Given a list of shares calculate the All Share Index
    '''
    value = 1.0
    acount = 0.0
    
    for thistock in allshares:
        if thistock.trades == None:
            continue
        value *= thistock.stockPrice()
        acount += 1    
    return pow(value,(1/acount))

if __name__ == '__main__':
    stocks = [ 
              aStock( 'TEA', COMMON, 100, 0 ),
              aStock( 'POP', COMMON, 100, 8),
              aStock( 'ALE', COMMON, 60, 23),
              aStock( 'GIN', PREF, 100, 8, .02),
              aStock(' JOE', COMMON, 250, 15)
              ]
    i = 1
    for mystock in stocks:
        mystock.recordTrade(10*i, 20*i, datetime.datetime.now() - datetime.timedelta(minutes=i), BUY) 
        i += 1  
        
    print "Yeild for %s " %stocks[3].symbol, stocks[3].currentYield( 100 )
    print "PE Ratio for %s" %stocks[1].symbol, stocks[1].peRatio(100)    
    print "Stock Price for %s" %stocks[2].symbol, stocks[2].stockPrice()
    print "All Share Index ", allShareIndex(stocks)

        
        