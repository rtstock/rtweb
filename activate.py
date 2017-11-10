from bottle import run,get, post, request,route, redirect
import requests
from flask import Flask, jsonify, request, render_template, Markup
import datetime
import numpy as np
import pandas as pd
import json
import io

app = Flask(__name__)

@route('/login')
def login():
    return '''
        <form action="/login" method="post">
            TickerString: <input name="tickerstring" type="text" />
            fromdate: <input name="fromdate" type="text" />
			todate: <input name="todate" type="text" />
            <input value="Login" type="submit" />
        </form>
    '''

@route('/login', method='POST')
def do_login():
    tickerstring = request.forms.get('tickerstring')
    fromdate = request.forms.get('fromdate')
    todate = request.forms.get('todate')
    #return redirect('http://localhost:8080/cov?tickerstring='+tickerstring+'&fromdate='+fromdate+'&todate='+todate, code=302)
    return redirect('http://localhost:8080/cov?tickerstring=MSFT-AAPL-KKR&fromdate=2017-09-01&todate=2017-09-30', code=302)	

from bottle import static_file
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='C:\Batches\GitStuff\websites\learnpost\wwwroot\output')

@route('/download/<filename:path>')
def download(filename):
    return static_file(filename, root='C:\Batches\GitStuff\websites\learnpost\wwwroot\output', download=filename)

@app.route('/cov')
def cov():
    try:
        print 'got here xx'
        todatestring = str(datetime.datetime.now().date())
        fromdatestring = todatestring[:-2] + '01'
        tickerstring = request.args.get('tickerstring', default = 'MSFT-AAPL', type = str)
        fromdatestring = request.args.get('fromdate', default = fromdatestring, type = str)
        todatestring = request.args.get('todate', default = todatestring, type = str)
    
        import pullstackedreturns as psp
        #symbols = ['MSFT','AMZN','GOOG','MS']
        symbols = tickerstring.split('-')
        fromdate,todate = fromdatestring,todatestring
        df_returns = psp.stockreturnsstacked(symbols,fromdate,todate,pricechangeortotal='pricechange')

        df_alignedpricechangereturns = df_returns
        df_alignedpricechangereturns = df_alignedpricechangereturns.dropna() #eeee
        
        covmatrix_array = np.cov(df_alignedpricechangereturns,None,0)
        rows = np.array(list(df_alignedpricechangereturns))[: np.newaxis]
        
        df = pd.DataFrame(covmatrix_array, index=rows, columns=list(df_alignedpricechangereturns))
        
        #df.index = df.index.map(str)
        list_of_dicts = df.T.to_dict()
        ret = jsonify({'cov': list_of_dicts})
    except Exception as inst:
        ret = 'Main.py My error was caught: ' + str(inst)
    return ret
	
run(host='localhost', port=8080, debug=True)