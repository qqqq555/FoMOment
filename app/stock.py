import pandas as pd
import requests 
import time
import json

def get_stock_info(stock_codes):
    stock_list_tse = [code for code in stock_codes if not code.startswith('6')]
    stock_list_otc = [code for code in stock_codes if code.startswith('6')]
    
    stock_list1 = '|'.join('tse_{}.tw'.format(stock) for stock in stock_list_tse) 
    stock_list2 = '|'.join('otc_{}.tw'.format(stock) for stock in stock_list_otc) 
    stock_list = stock_list1 + '|' + stock_list2

    query_url = f'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={stock_list}'
    response = requests.get(query_url)

    if response.status_code != 200:
        return None
    
    data = json.loads(response.text)
    columns = ['c','n','z','tv','v','o','h','l','y', 'tlong']
    df = pd.DataFrame(data['msgArray'], columns=columns)
    df.columns = ['股票代號','公司簡稱','成交價','成交量','累積成交量','開盤價','最高價','最低價','昨收價', '資料更新時間']
    df.insert(9, "漲跌百分比", 0.0)

    def count_per(x):
        if isinstance(x[0], int) == False:
            x[0] = 0.0
        result = (x[0] - float(x[1])) / float(x[1]) * 100
        return pd.Series(['-' if x[0] == 0.0 else x[0], x[1], '-' if result == -100 else result])

    df[['成交價', '昨收價', '漲跌百分比']] = df[['成交價', '昨收價', '漲跌百分比']].apply(count_per, axis=1)

    def time2str(t):
        try:
            t = int(float(t)) / 1000 + 8 * 60 * 60
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        except (ValueError, TypeError):
            return "Invalid timestamp"
    
    df['資料更新時間'] = df['資料更新時間'].apply(time2str)
    
    return df

def format_stock_info(stock_info):
    return (f"股票代號: {stock_info['股票代號']}\n"
            f"公司簡稱: {stock_info['公司簡稱']}\n"
            f"成交價: {stock_info['成交價']}\n"
            f"成交量: {stock_info['成交量']}\n"
            f"累積成交量: {stock_info['累積成交量']}\n"
            f"開盤價: {stock_info['開盤價']}\n"
            f"最高價: {stock_info['最高價']}\n"
            f"最低價: {stock_info['最低價']}\n"
            f"昨收價: {stock_info['昨收價']}\n"
            f"漲跌百分比: {stock_info['漲跌百分比']:.2f}%\n"
            f"資料更新時間: {stock_info['資料更新時間']}")
