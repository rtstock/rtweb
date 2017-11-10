import pandas as pd
import numpy as np
def stockreturnsstacked(symbols,fromdate,todate,pricechangeortotal='pricechange',logorarithmetic='log'):
    import pullstackedprices as psp
    df_00 = psp.stockpricesstacked(symbols,fromdate,todate,pricechangeortotal)
    df_01 = pd.DataFrame(index=df_00.index.copy())
    list_of_symbols_good = list(df_00.columns)
    print 'list_of_symbols_good',list_of_symbols_good
    for s in list_of_symbols_good:
        if not logorarithmetic == 'log':
            df_01[s] = df_00[s].pct_change()
        else:
            df_01[s] = np.log(1.0 + df_00[s].pct_change())        
    return df_01

if __name__=='__main__':
    symbols = ['MAR', 'MON', 'NOV', 'A', 'AAL', 'AAP', 'AAPL', ]
    print 'symbols',symbols
    df = stockreturnsstacked(symbols,'2017-07-01','2017-11-09')
    print df
