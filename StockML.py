from __future__ import division
import pandas as pd
import os
import time
from datetime import datetime
import numpy as np
from sklearn import svm, preprocessing
import quandl
import statistics
import warnings



warnings.filterwarnings("ignore")



from time import mktime
import matplotlib.pyplot as plt

import re
auth_tok = "cBs2HV_F6r9ybCynEToS"
# data = quandl.get("WIKI/KO", trim_start = "2000-12-12", trim_end = "2014-12-12", auth_token = auth_tok)
# print(data)
print(np.version.version)

def StockPrices():
    df = pd.DataFrame()
    statspath = path+'/_KeyStats'
    stockList = [x[0] for x in os.walk(statspath)]

    try:
        for each_dir in stockList[1:]:
            ticker = each_dir.split('/')[-1]
            if ticker == "act":
                continue
            print(ticker)
            name = "WIKI/"+ticker.upper()
            data = quandl.get(name, trim_start = "2000-12-12", trim_end = "2014-12-12", auth_token = auth_tok)
            data[ticker.upper()] = data["Adj. Close"]
            df = pd.concat([df, data[ticker.upper()]], axis=1)
    except Exception as e:
        print(ticker)
        print (str(e))
        # try:
        #     for each_dir in stockList[1:]:
        #         ticker = each_dir.split("\\")[1]
        #         print(ticker)
        #         name = "WIKI/" + ticker.upper()
        #         data = quandl.get(name, trim_start="2000-12-12", trim_end="2014-12-12", auth_token=auth_tok)
        #         data[ticker.upper()] = data["Adj. Close"]
        #         df = pd.concat([df, data[ticker.upper()]], axis=1)
        # except Exception as e:
        #     print(str(e))

    df.to_csv("stock_prices.csv")

FEATURES = ['DE Ratio',
            'Trailing P/E',
            'Price/Sales',
            'Price/Book',
            'Profit Margin',
            'Operating Margin',
            'Return on Assets',
            'Return on Equity',
            'Revenue Per Share',
            'Market Cap',
            'Enterprise Value',
            'Forward P/E',
            'PEG Ratio',
            'Enterprise Value/Revenue',
            'Enterprise Value/EBITDA',
            'Revenue',
            'Gross Profit',
            'EBITDA',
            'Net Income Avl to Common ',
            'Diluted EPS',
            'Earnings Growth',
            'Revenue Growth',
            'Total Cash',
            'Total Cash Per Share',
            'Total Debt',
            'Current Ratio',
            'Book Value Per Share',
            'Cash Flow',
            'Beta',
            'Held by Insiders',
            'Held by Institutions',
            'Shares Short (as of',
            'Short Ratio',
            'Short % of Float',
            'Shares Short (prior ']


path = "/Users/Nico/Downloads/intraQuarter"

def Key_Stats(gather=["Total Debt/Equity",
                      'Trailing P/E',
                      'Price/Sales',
                      'Price/Book',
                      'Profit Margin',
                      'Operating Margin',
                      'Return on Assets',
                      'Return on Equity',
                      'Revenue Per Share',
                      'Market Cap',
                        'Enterprise Value',
                        'Forward P/E',
                        'PEG Ratio',
                        'Enterprise Value/Revenue',
                        'Enterprise Value/EBITDA',
                        'Revenue',
                        'Gross Profit',
                        'EBITDA',
                        'Net Income Avl to Common ',
                        'Diluted EPS',
                        'Earnings Growth',
                        'Revenue Growth',
                        'Total Cash',
                        'Total Cash Per Share',
                        'Total Debt',
                        'Current Ratio',
                        'Book Value Per Share',
                        'Cash Flow',
                        'Beta',
                        'Held by Insiders',
                        'Held by Institutions',
                        'Shares Short (as of',
                        'Short Ratio',
                        'Short % of Float',
                        'Shares Short (prior ']):

    statspath = path+'/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    df = pd.DataFrame(columns = ['Date',
                                 'Unix',
                                 'Ticker',
                                 'Price',
                                 'stock_p_change',
                                 'SP500',
                                 'sp500_p_change',
                                 'Difference',
                                 ##############
                                 'DE Ratio',
                                 'Trailing P/E',
                                 'Price/Sales',
                                 'Price/Book',
                                 'Profit Margin',
                                 'Operating Margin',
                                 'Return on Assets',
                                 'Return on Equity',
                                 'Revenue Per Share',
                                 'Market Cap',
                                 'Enterprise Value',
                                 'Forward P/E',
                                 'PEG Ratio',
                                 'Enterprise Value/Revenue',
                                 'Enterprise Value/EBITDA',
                                 'Revenue',
                                 'Gross Profit',
                                 'EBITDA',
                                 'Net Income Avl to Common ',
                                 'Diluted EPS',
                                 'Earnings Growth',
                                 'Revenue Growth',
                                 'Total Cash',
                                 'Total Cash Per Share',
                                 'Total Debt',
                                 'Current Ratio',
                                 'Book Value Per Share',
                                 'Cash Flow',
                                 'Beta',
                                 'Held by Insiders',
                                 'Held by Institutions',
                                 'Shares Short (as of',
                                 'Short Ratio',
                                 'Short % of Float',
                                 'Shares Short (prior ',
                                 ##############
                                 'Status'])

    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")
    stockPrice_df = pd.DataFrame.from_csv("StockPrices.csv")

    ticker_list = []

    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        ticker = each_dir.split("/_KeyStats/")[1]
        ticker_list.append(ticker)

        # starting_stock_value = False
        # starting_sp500_value = False


        if len(each_file) > 0:
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                full_file_path = each_dir + '/' + file
                source = open(full_file_path, 'r').read()
                try:
                    value_list = []

                    for each_data in gather:
                        try:
                            regex = re.escape(each_data) + r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?'
                            value = re.search(regex, source)
                            value = (value.group(1))

                            if "B" in value:
                                value = float(value.replace("B", '')) * 1000000000

                            elif "M" in value:
                                value = float(value.replace("M", '')) * 1000000

                            value_list.append(value)


                        except Exception as e:
                            value = "N/A"
                            value_list.append(value)

                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                    except:
                        try:
                            sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
                            row = sp500_df[(sp500_df.index == sp500_date)]
                            sp500_value = float(row["Adjusted Close"])
                        except Exception as e:
                            print("fapsdolkfhasf;lsak", str(e))

                    one_year_later = int(unix_time + 31536000)

                    try:
                        sp500_1y = datetime.fromtimestamp(one_year_later).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_1y)]
                        sp500_1y_value = float(row["Adjusted Close"])
                    except:
                        try:
                            sp500_1y = datetime.fromtimestamp(one_year_later - 259200).strftime('%Y-%m-%d')
                            row = sp500_df[(sp500_df.index == sp500_1y)]
                            sp500_1y_value = float(row["Adjusted Close"])
                        except Exception as e:
                            print("sp500 1 year later issue", str(e))

                    try:
                        stock_price_1y = datetime.fromtimestamp(one_year_later).strftime('%Y-%m-%d')
                        row = stockPrice_df[(stockPrice_df.index == stock_price_1y)][ticker.upper()]

                        stock_1y_value = round(float(row), 2)
                        ##                        print(stock_1y_value)
                        ##                        time.sleep(1555)

                    except Exception as e:
                        try:
                            stock_price_1y = datetime.fromtimestamp(one_year_later - 259200).strftime('%Y-%m-%d')
                            row = stockPrice_df[(stockPrice_df.index == stock_price_1y)][ticker.upper()]
                            stock_1y_value = round(float(row), 2)
                        except Exception as e:
                            print("stock price:", str(e))

                    try:
                        stock_price = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = stockPrice_df[(stockPrice_df.index == stock_price)][ticker.upper()]
                        stock_price = round(float(row), 2)

                    except Exception as e:
                        try:
                            stock_price = datetime.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
                            row = stockPrice_df[(stockPrice_df.index == stock_price)][ticker.upper()]
                            stock_price = round(float(row), 2)
                        except Exception as e:
                            print("stock price:", str(e))

                    stock_p_change = round((((stock_1y_value - stock_price) / stock_price) * 100), 2)
                    sp500_p_change = round((((sp500_1y_value - sp500_value) / sp500_value) * 100), 2)

                    difference = stock_p_change - sp500_p_change

                    if difference > 0:
                        status = "outperform"
                    else:
                        status = "underperform"

                    if value_list.count("N/A") > 0:
                        pass
                    else:

                        df = df.append({'Date': date_stamp,
                                        'Unix': unix_time,
                                        'Ticker': ticker,

                                        'Price': stock_price,
                                        'stock_p_change': stock_p_change,
                                        'SP500': sp500_value,
                                        'sp500_p_change': sp500_p_change,
                                        'Difference': difference,
                                        'DE Ratio': value_list[0],
                                        # 'Market Cap':value_list[1],
                                        'Trailing P/E': value_list[1],
                                        'Price/Sales': value_list[2],
                                        'Price/Book': value_list[3],
                                        'Profit Margin': value_list[4],
                                        'Operating Margin': value_list[5],
                                        'Return on Assets': value_list[6],
                                        'Return on Equity': value_list[7],
                                        'Revenue Per Share': value_list[8],
                                        'Market Cap': value_list[9],
                                        'Enterprise Value': value_list[10],
                                        'Forward P/E': value_list[11],
                                        'PEG Ratio': value_list[12],
                                        'Enterprise Value/Revenue': value_list[13],
                                        'Enterprise Value/EBITDA': value_list[14],
                                        'Revenue': value_list[15],
                                        'Gross Profit': value_list[16],
                                        'EBITDA': value_list[17],
                                        'Net Income Avl to Common ': value_list[18],
                                        'Diluted EPS': value_list[19],
                                        'Earnings Growth': value_list[20],
                                        'Revenue Growth': value_list[21],
                                        'Total Cash': value_list[22],
                                        'Total Cash Per Share': value_list[23],
                                        'Total Debt': value_list[24],
                                        'Current Ratio': value_list[25],
                                        'Book Value Per Share': value_list[26],
                                        'Cash Flow': value_list[27],
                                        'Beta': value_list[28],
                                        'Held by Insiders': value_list[29],
                                        'Held by Institutions': value_list[30],
                                        'Shares Short (as of': value_list[31],
                                        'Short Ratio': value_list[32],
                                        'Short % of Float': value_list[33],
                                        'Shares Short (prior ': value_list[34],
                                        'Status': status},
                                       ignore_index=True)
                except Exception as e:
                    pass

    df.to_csv("key_stats_acc_perf_WITH_NA.csv")




def Build_Data_Set():

    data_df = pd.DataFrame.from_csv("key_stats_acc_perf_WITH_NA.csv")
    #data_df = data_df[:100]

    data_df = data_df.reindex(np.random.permutation(data_df.index))
    data_df = data_df.replace("NaN",0).replace("N/A",0)

    X = np.array(data_df[FEATURES].values)
    Y = (data_df["Status"]
         .replace("underperform", 0)
         .replace("outperform", 1)
         .values.tolist())
    X = preprocessing.scale(X)

    Z = np.array(data_df[["stock_p_change", 'sp500_p_change']])
    return X, Y, Z

def Analysis():


    # test_size = 1000
    # X, Y, Z = Build_Data_Set()
    # print(len(X))
    #
    # clf = svm.SVC(kernel="linear", C=1.0)
    # clf.fit(X[:-test_size], Y[:-test_size])
    #
    # correct_count = np.sum(clf.predict(X[-test_size:]) == Y[-test_size:])
    #
    # if clf.predict(X[-x])[0] == 1:
    #
    #
    # print("Accuracy:", (correct_count/test_size)*100.00)
    test_size = 1200

    invest_amount = 10000
    total_invests = 0
    if_market = 0
    if_strat = 0
    amountInvested = 0

    X, y, Z = Build_Data_Set()
    print(len(X))

    clf = svm.SVC(kernel="linear", C=1.0)
    clf.fit(X[:-test_size], y[:-test_size])

    correct_count = 0

    for x in range(1, test_size + 1):
        if clf.predict(X[-x])[0] == y[-x]:
            correct_count += 1
            # time.sleep(1)

        if clf.predict(X[-x])[0] == 1:
            # time.sleep(1)
            amountInvested += invest_amount

            invest_return = invest_amount + (invest_amount * (Z[-x][0] / 100))
            market_return = invest_amount + (invest_amount * (Z[-x][1] / 100))
            total_invests += 1
            if_market += market_return
            if_strat += invest_return

    print("Accuracy:", (correct_count / test_size) * 100.00)

    print("Total Trades:", total_invests)
    print("Ending with Strategy:", if_strat)
    print("Ending with Market:", if_market)

    compared = ((if_strat - if_market) / if_market) * 100.0
    do_nothing = total_invests * invest_amount

    avg_market = ((if_market - do_nothing) / do_nothing) * 100.0
    avg_strat = ((if_strat - do_nothing) / do_nothing) * 100.0

    print("Compared to market, we earn", str(compared) + "% more")
    print("Average investment return:", str(avg_strat) + "%")
    print("Average market return:", str(avg_market) + "%")
    print("Total amount invested: ", str(amountInvested))





#Key_Stats()

Analysis()

#StockPrices()


