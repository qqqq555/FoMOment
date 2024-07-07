import requests
import pandas as pd
import io

def get_stock_info(stock_code):
    # Fetch all stock data from STOCK_DAY_ALL
    url_day_all = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=open_data'
    response_day_all = requests.get(url_day_all)
    
    if response_day_all.status_code != 200:
        return f"Error: Unable to fetch data (Status Code: {response_day_all.status_code})"
    
    # Load data into a DataFrame
    data_day_all = response_day_all.text
    df_day_all = pd.read_csv(io.StringIO(data_day_all))
    
    # Filter the DataFrame for the specific stock code
    stock_data = df_day_all[df_day_all['證券代號'] == stock_code]
    
    if stock_data.empty:
        return "找不到該股票資訊。"
    
    # Get the most recent stock data
    stock_data = stock_data.iloc[-1]
    
    # Extract necessary information from STOCK_DAY_ALL
    columns = ['證券代號', '證券名稱', '收盤價', '成交股數', '開盤價', '最高價', '最低價']
    stock_data = stock_data[columns]
    
    # Fetch additional information from TWT84U
    url_twt84u = f'https://openapi.twse.com.tw/v1/exchangeReport/TWT84U?stockNo={stock_code}'
    response_twt84u = requests.get(url_twt84u)
    
    if response_twt84u.status_code != 200:
        return f"Error: Unable to fetch additional data (Status Code: {response_twt84u.status_code})"
    
    data_twt84u = response_twt84u.json()
    
    if not data_twt84u:
        return "找不到該股票的額外資訊。"
    
    # Find the correct record in the TWT84U data
    additional_data = None
    for record in data_twt84u:
        if record.get('Code') == stock_code:
            additional_data = record
            break
    
    if additional_data is None:
        return "找不到該股票的額外資訊。"
    
    # Calculate 漲跌百分比
    previous_day_price = additional_data.get('PreviousDayPrice')
    current_price = stock_data['收盤價']
    
    if previous_day_price and current_price:
        try:
            previous_day_price = float(previous_day_price)
            current_price = float(current_price)
            percent_change = (current_price - previous_day_price) / previous_day_price * 100
        except ValueError:
            percent_change = None
    else:
        percent_change = None
    
    # Format the stock information
    info = f"股票代號: {stock_data['證券代號']}\n"
    info += f"公司簡稱: {stock_data['證券名稱']}\n"
    info += f"成交價: {stock_data['收盤價']}\n"
    if percent_change is not None:
        info += f"漲跌百分比: {percent_change:.2f}%\n"
    else:
        info += f"漲跌百分比: N/A\n"
    info += f"成交量: {stock_data['成交股數']}\n"
    info += f"開盤價: {stock_data['開盤價']}\n"
    info += f"最高價: {stock_data['最高價']}\n"
    info += f"最低價: {stock_data['最低價']}\n"
    
    # Add additional information from TWT84U
    info += f"本日漲停價: {additional_data.get('TodayLimitUp', 'N/A')}\n"
    info += f"本日開盤競價基準: {additional_data.get('TodayOpeningRefPrice', 'N/A')}\n"
    info += f"本日跌停價: {additional_data.get('TodayLimitDown', 'N/A')}\n"
    info += f"前日開盤競價基準: {additional_data.get('PreviousDayOpeningRefPrice', 'N/A')}\n"
    info += f"前日收盤價: {additional_data.get('PreviousDayPrice', 'N/A')}\n"
    info += f"前日買進揭示價: {additional_data.get('PreviousDayLimitUp', 'N/A')}\n"
    info += f"前日賣出揭示價: {additional_data.get('PreviousDayLimitDown', 'N/A')}\n"
    info += f"最近成交日: {additional_data.get('LastTradingDay', 'N/A')}\n"
    
    return info

# Example usage:
stock_code = '0050'
print(get_stock_info(stock_code))

'''
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
