import pandas as pd
import requests
import json
import datetime

def get_stock_info(stock_code):
    # Determine if it's an OTC stock (starts with '6')
    if stock_code.startswith('6'):
        stock_list = f'otc_{stock_code}.tw'
    else:
        stock_list = f'tse_{stock_code}.tw'

    query_url = f'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={stock_list}'
    
    response = requests.get(query_url)
    if response.status_code == 404 OR response.status_code == 500:
        return "取得股票資訊失敗。"
    
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