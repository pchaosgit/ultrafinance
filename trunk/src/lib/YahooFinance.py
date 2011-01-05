'''
Created on Dec 21, 2010

@author: ppa

Thanks to Corey Goldberg, this module is based http://www.goldb.org/ystockquote.html
sample usage:
>>> import YahooFinance
>>> print YahooFinance.get_price('GOOG')
529.46
'''
import urllib
from operator import itemgetter

class YahooFinance():
    def __request(self, symbol, stat):
        url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
        return urllib.urlopen(url).read().strip().strip('"')

    def get_all(self, symbol):
        """
        Get all available quote data for the given ticker symbol.
        Returns a dictionary.
        """
        values = self.__request(symbol, 'l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7').split(',')
        data = {}
        data['price'] = values[0]
        data['change'] = values[1]
        data['volume'] = values[2]
        data['avg_daily_volume'] = values[3]
        data['stock_exchange'] = values[4]
        data['market_cap'] = values[5]
        data['book_value'] = values[6]
        data['ebitda'] = values[7]
        data['dividend_per_share'] = values[8]
        data['dividend_yield'] = values[9]
        data['earnings_per_share'] = values[10]
        data['52_week_high'] = values[11]
        data['52_week_low'] = values[12]
        data['50day_moving_avg'] = values[13]
        data['200day_moving_avg'] = values[14]
        data['price_earnings_ratio'] = values[15]
        data['price_earnings_growth_ratio'] = values[16]
        data['price_sales_ratio'] = values[17]
        data['price_book_ratio'] = values[18]
        data['short_ratio'] = values[19]
        return data
        
    def get_price(self, symbol): 
        return self.__request(symbol, 'l1')
    
    def get_change(self, symbol):
        return self.__request(symbol, 'c1')
        
    def get_volume(self, symbol): 
        return self.__request(symbol, 'v')
    
    def get_avg_daily_volume(self, symbol): 
        return self.__request(symbol, 'a2')
        
    def get_stock_exchange(self, symbol): 
        return self.__request(symbol, 'x')
         
    def get_market_cap(self, symbol):
        return self.__request(symbol, 'j1')
       
    def get_book_value(self, symbol):
        return self.__request(symbol, 'b4')
    
    def get_ebitda(self, symbol): 
        return self.__request(symbol, 'j4')
        
    def get_dividend_per_share(self, symbol):
        return self.__request(symbol, 'd')
    
    def get_dividend_yield(self, symbol): 
        return self.__request(symbol, 'y')
        
    def get_earnings_per_share(self, symbol): 
        return self.__request(symbol, 'e')
    
    def get_52_week_high(self, symbol): 
        return self.__request(symbol, 'k')
        
    def get_52_week_low(self, symbol): 
        return self.__request(symbol, 'j')
    
    def get_50day_moving_avg(self, symbol): 
        return self.__request(symbol, 'm3')
        
    def get_200day_moving_avg(self, symbol):
        return self.__request(symbol, 'm4')
        
    def get_price_earnings_ratio(self, symbol): 
        return self.__request(symbol, 'r')
    
    def get_price_earnings_growth_ratio(self, symbol): 
        return self.__request(symbol, 'r5')
    
    def get_price_sales_ratio(self, symbol): 
        return self.__request(symbol, 'p5')
        
    def get_price_book_ratio(self, symbol): 
        return self.__request(symbol, 'p6')

    def get_short_ratio(self, symbol): 
        return self.__request(symbol, 's7')
        
    def get_historical_prices(self, symbol, start_date, end_date):
        """
        Get historical prices for the given ticker symbol.
        Date format is 'YYYYMMDD'
    
        Returns a nested list.
        """
        url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
            'd=%s&' % str(int(end_date[4:6]) - 1) + \
            'e=%s&' % str(int(end_date[6:8])) + \
            'f=%s&' % str(int(end_date[0:4])) + \
            'g=d&' + \
            'a=%s&' % str(int(start_date[4:6]) - 1) + \
            'b=%s&' % str(int(start_date[6:8])) + \
            'c=%s&' % str(int(start_date[0:4])) + \
            'ignore=.csv'
        days = urllib.urlopen(url).readlines()
        data = [day[:-2].split(',') for day in days]
        return data

    def get_dates_values(self, symbol, start_date, end_date):
        values = self.get_historical_prices(symbol, \
                                            str(start_date).replace('-', ''), 
                                            str(end_date).replace('-', ''))
        data = {}
        for value in values[1:]:
            data[value[0]] = (value[4], value[6])
        
        dateValues = sorted(data.items(), key=itemgetter(0))
        return dateValues

if __name__ == '__main__':
    yahooFinance = YahooFinance()
    print yahooFinance.get_historical_prices('SPY', '199000101', '20100101')