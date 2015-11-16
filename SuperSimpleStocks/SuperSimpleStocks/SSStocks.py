'''
Created on 15 Nov 2015

@author: Allan Clearwaters

Super Simple Stocks - Python 2.7.10
'''
from datetime import *
import datetime
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
#    price = float(0)
#    quantity = 0
#    dtme = datetime.datetime(1, 1, 1)
#    ttype = BUY     # True => buy, False => sell
    
    def __init__(self, quant, price, dtme=datetime.datetime(1, 1, 1), ttype=BUY):
        self.price = int(price)
        self.quantity = int(quant)
        # Make sure the date tag is in the right format
        self.dtme = dtme
        self.type = ttype
        
class CommonStock(object):
    '''
    The class for individual stocks
    Common stoack are always valid, Preferred stock is valid
    only if the fixed dividend != None
    '''
#    symbol = ''       # What to call it
#    lastDividend = (0)     # The last dividend
#    parValue = (0)        # Current par value
#    trades = None             #List of trades
    name = 'common'
    
    def __init__(self, symb, parval, dividend ):
        '''
        Symbol and type are not optional
        The rest are optional
        '''
        self.symbol = symb
        self.parValue = int(parval)
        self.lastDividend = int(dividend)
        self.trades = None
    
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
        return self.lastDividend/float(tickerPrice)
    
    def peRatio(self, tickerPrice ):
        ''' Calculate the pe ratio
        '''
        return (float(tickerPrice)/float(self.lastDividend)) if self.lastDividend != None else (0.0)
    
    def stockPrice(self):
        '''  Calculate the price. Return None if there are no trades
        '''
        acount = 0
        asum = 0
        
        # What is the date range
        dtend = datetime.datetime.now()
        dwindow = datetime.timedelta(minutes=15)
        
        if self.trades == None:
            return 0
        
        for thistrade in self.trades:
            if (dtend - thistrade.dtme) < dwindow:
                asum += thistrade.price * thistrade.quantity
                acount += thistrade.quantity
        return int(float(asum)/float(acount))
    
class PreferredStock( CommonStock ):
    ''' The class of preferred stock
    '''
    name = 'preferred'
    
    def __init__(self, symb, parval, dividend, fdividend ):
        # super initialization
        CommonStock.__init__(self, symb, parval, dividend)
        self.fixedDividend = float(fdividend)
        self.name = 'preferred'
        
    def currentYield(self, tickerPrice ):
        ''' Calculate the yield
        '''
        return self.fixedDividend*self.parValue/float(tickerPrice)

def allShareIndex( allshares ):
    ''' Given a list of shares calculate the All Share Index
    '''
    value = 1.0
    acount = 0
    
    for thistock in allshares:
        if thistock.trades == None:
            continue
        value *= thistock.stockPrice()
        acount += 1  
    return pow(value,(1/float(acount)) )    
        
if __name__ == '__main__':
    stocks = [ 
              CommonStock('TEA', 100, 0 ),
              CommonStock( 'POP', 100, 8),
              CommonStock( 'ALE', 60, 23),
              PreferredStock( 'GIN', 100, 8, .02),
              CommonStock('JOE', 250, 15)
              ]

    index = 1
    for mystock in stocks:
        mystock.recordTrade(10*index, 20*index, datetime.datetime.now() - datetime.timedelta(minutes=index), BUY) 
        mystock.recordTrade(13*index, 6*index, datetime.datetime.now() - datetime.timedelta(minutes=(index+1)), BUY) 
        mystock.recordTrade(31*index, 55*index, datetime.datetime.now() - datetime.timedelta(minutes=(index+3)), SELL)       
        index += 1 
        
    print "Yeild for %s %s" %(stocks[3].symbol, stocks[3].name), stocks[3].currentYield( 100 )
    print "Yeild for %s %s" %(stocks[2].symbol, stocks[2].name), stocks[2].currentYield( 100 )
    print "PE Ratio for %s" %stocks[1].symbol, stocks[1].peRatio(100)    
    print "Stock Price for %s" %stocks[2].symbol, stocks[2].stockPrice()
    print "All Share Index ", allShareIndex(stocks)

        
        