import requests
import json
import pandas as pd
import datetime

def get_stock_info(stock_code):
    if stock_code.startswith('6'):
        stock_list = f'otc_{stock_code}.tw'
    else:
        stock_list = f'tse_{stock_code}.tw'
    
    query_url = f'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={stock_list}'
    response = requests.get(query_url)
    
    if response.status_code != 200:
        return response.status_code
    
    data = json.loads(response.text)
    if not data['msgArray']:
        return "找不到該股票資訊。"
    
    stock_data = data['msgArray'][0]
    columns = ['c', 'n', 'z', 'tv', 'v', 'o', 'h', 'l', 'y', 'tlong']
    df = pd.DataFrame([stock_data], columns=columns)
    df.columns = ['股票代號', '公司簡稱', '成交價', '成交量', '累積成交量', '開盤價', '最高價', '最低價', '昨收價', '資料更新時間']
    
    # Handle cases where some values might be '-'
    for col in ['成交價', '昨收價']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    if pd.notna(df['成交價'].values[0]) and pd.notna(df['昨收價'].values[0]):
        df['漲跌百分比'] = (df['成交價'].values[0] - df['昨收價'].values[0]) / df['昨收價'].values[0] * 100
    else:
        df['漲跌百分比'] = None
    
    df['資料更新時間'] = pd.to_datetime(int(df['資料更新時間'].values[0]) / 1000 + 8 * 3600, unit='s').strftime('%Y-%m-%d %H:%M:%S')
    
    info = f"股票代號: {df['股票代號'].values[0]}\n"
    info += f"公司簡稱: {df['公司簡稱'].values[0]}\n"
    info += f"成交價: {df['成交價'].values[0]}\n"
    
    if pd.notna(df['漲跌百分比'].values[0]):
        info += f"漲跌百分比: {df['漲跌百分比'].values[0]:.2f}%\n"
    else:
        info += "漲跌百分比: N/A\n"
    
    info += f"成交量: {df['成交量'].values[0]}\n"
    info += f"開盤價: {df['開盤價'].values[0]}\n"
    info += f"最高價: {df['最高價'].values[0]}\n"
    info += f"最低價: {df['最低價'].values[0]}\n"
    info += f"昨收價: {df['昨收價'].values[0]}\n"
    info += f"更新時間: {df['資料更新時間'].values[0]}"
    
    return info

print(get_stock_info('2330'))


'''
import twstock
import pandas as pd
import datetime

def get_stock_info(stock_code):
    try:
        print(f"Fetching real-time data for stock code: {stock_code}")
        stock = twstock.realtime.get(stock_code)
        print(f"Stock data fetched: {stock}")

        if stock and stock['success']:
            # Extract data and calculate the price change percentage
            open_price = float(stock['realtime'].get('open', 0))
            current_price = float(stock['realtime'].get('latest_trade_price', 0))
            if open_price != 0:
                change_percent = (current_price - open_price) / open_price * 100
            else:
                change_percent = None

            # Create a DataFrame with the fetched data
            data = {
                '股票代號': [stock_code],
                '公司簡稱': [stock['info'].get('name', 'N/A')],
                '成交價': [current_price],
                '漲跌百分比': [change_percent],
                '成交量': [stock['realtime'].get('accumulate_trade_volume', 'N/A')],
                '開盤價': [open_price],
                '最高價': [stock['realtime'].get('high', 'N/A')],
                '最低價': [stock['realtime'].get('low', 'N/A')],
                '昨收價': [stock['realtime'].get('yesterday_close', 'N/A')],
                '資料更新時間': [datetime.datetime.fromtimestamp(int(stock['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')]
            }

            df = pd.DataFrame(data)

            # Format the information
            info = f"股票代號: {df['股票代號'].values[0]}\n"
            info += f"公司簡稱: {df['公司簡稱'].values[0]}\n"
            info += f"成交價: {df['成交價'].values[0]}\n"
            
            if pd.notna(df['漲跌百分比'].values[0]):
                info += f"漲跌百分比: {df['漲跌百分比'].values[0]:.2f}%\n"
            else:
                info += "漲跌百分比: N/A\n"
            
            info += f"成交量: {df['成交量'].values[0]}\n"
            info += f"開盤價: {df['開盤價'].values[0]}\n"
            info += f"最高價: {df['最高價'].values[0]}\n"
            info += f"最低價: {df['最低價'].values[0]}\n"
            info += f"昨收價: {df['昨收價'].values[0]}\n"
            info += f"更新時間: {df['資料更新時間'].values[0]}"
            
            return info
        else:
            return "無法獲取即時股票資訊。"
    except Exception as e:
        print(f"發生錯誤：{str(e)}")
        # Return a default message or indication of failure
        return "抱歉，無法獲取股票資訊。"

# Example usage:
stock_code = '2330'
print(get_stock_info(stock_code))
'''


'''
target_stock = '0050'  # 股票代號變數
stock = twstock.Stock(target_stock)  # 告訴twstock我們要查詢的股票
target_price = stock.fetch_from(2020, 5)  # 取用2020/05至今每天的交易資料

name_attribute = [
    'Date', 'Capacity', 'Turnover', 'Open', 'High', 'Low', 'Close', 'Change', 'Transaction'
]  # 幫收集到的資料設定表頭

df = pd.DataFrame(columns=name_attribute, data=target_price)
# 將twstock抓到的清單轉成Data Frame格式的資料表

filename = f'./data/{target_stock}.csv'
# 指定Data Frame轉存csv檔案的檔名與路徑

df.to_csv(filename)
# 將Data Frame轉存為csv檔案

# Fetch and print real-time stock info
print(get_stock_info(target_stock))
'''
