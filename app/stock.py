'''import pandas as pd
import requests
import json
import datetime'''

'''def get_kline():
    target_stock = '2330'  #股票代號變數
    stock = twstock.Stock(target_stock)  #告訴twstock我們要查詢的股票
    target_price = stock.fetch_from(2022, 5)  #取用2020/05至今每天的交易資料

    name_attribute = [
        'Date', 'Capacity', 'Volume', 'Open', 'High', 'Low', 'Close', 'Change',
        'Transcation'
    ]  #幫收集到的資料設定表頭

    df = pd.DataFrame(columns=name_attribute, data=target_price)
    #將twstock抓到的清單轉成Data Frame格式的資料表

    filename = f'./data/{target_stock}.csv'
    #指定Data Frame轉存csv檔案的檔名與路徑

    df.to_csv(filename)
    #將Data Frame轉存為csv檔案

    # 導入pandas、matplotlib、mplfinance模組，將mplfinance模組縮寫為mpf
    # 這邊要導入matplotlib的原因是因為mplfinance繪圖時需要調用mptplotlib模組

    target_stock = '2330' #設定要繪製走勢圖的股票

    df = pd.read_csv(f'./data/{target_stock}.csv', parse_dates=True, index_col=1) #讀取目標股票csv檔的位置

    df.rename(columns={'Turnover':'Volume'}, inplace = True) 
    #這裡針對資料表做一下修正，因為交易量(Turnover)在mplfinance中須被改為Volume才能被認出來

    mc = mpf.make_marketcolors(up='r',down='g',inherit=True)
    s  = mpf.make_mpf_style(base_mpf_style='yahoo',marketcolors=mc)
    #針對線圖的外觀微調，將上漲設定為紅色，下跌設定為綠色，符合台股表示習慣
    #接著把自訂的marketcolors放到自訂的style中，而這個改動是基於預設的yahoo外觀

    kwargs = dict(type='candle', mav=(5,20,60), volume=True, figratio=(10,8), figscale=0.75, title=target_stock, style=s) 
    #設定可變參數kwargs，並在變數中填上繪圖時會用到的設定值

    mpf.plot(df, **kwargs)
    #選擇df資料表為資料來源，帶入kwargs參數，畫出目標股票的走勢圖


    if not os.path.exists('data'):
        os.makedirs('data')

    target_stock = '2330'
    stock = twstock.Stock(target_stock)
    target_price = stock.fetch_from(2020, 5)
    name_attribute = [
        'Date', 'Capacity', 'Volume', 'Open', 'High', 'Low', 'Close', 'Change',
        'Transaction'
    ]
    df = pd.DataFrame(columns=name_attribute, data=target_price)
    filename = f'./data/{target_stock}.csv'
    df.to_csv(filename)

    df = pd.read_csv(f'./data/{target_stock}.csv', parse_dates=True, index_col=1)
    df.rename(columns={'Turnover':'Volume'}, inplace=True)

    mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
    s = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
    kwargs = dict(type='candle', mav=(5,20,60), volume=True, figratio=(10,8), figscale=0.75, title=target_stock, style=s)

    # Create a buffer to store the image
    buf = io.BytesIO()

    # Save the plot to the buffer instead of displaying it
    mpf.plot(df, **kwargs, savefig=dict(fname=buf, format='png'))
    buf.seek(0)

    # Set up the Google Cloud Storage client
    storage_client = storage.Client()
    bucket_name = 'sitconimg'  # Replace with your actual bucket name
    bucket = storage_client.bucket(bucket_name)

    # Create a blob and upload the image
    blob = bucket.blob(f'kline_images/{target_stock}.png')
    blob.upload_from_file(buf, content_type='image/png')

    # Make the blob publicly accessible (optional)
    blob.make_public()

    # Get the public URL
    public_url = blob.public_url
    print(f"Image uploaded to: {public_url}") '''

import twstock
import datetime

def get_stock_info(stock_code):
    try:
        stock = twstock.realtime.get(stock_code)
        
        if stock['success']:
            info = f"股票代號: {stock_code}\n"
            info += f"公司簡稱: {stock['info']['name']}\n"
            info += f"成交價: {stock['realtime']['latest_trade_price']}\n"
            
            # Calculate price change percentage
            open_price = float(stock['realtime']['open'])
            current_price = float(stock['realtime']['latest_trade_price'])
            if open_price != 0:
                change_percent = (current_price - open_price) / open_price * 100
                info += f"漲跌百分比: {change_percent:.2f}%\n"
            else:
                info += "漲跌百分比: N/A\n"
            
            info += f"成交量: {stock['realtime']['accumulate_trade_volume']}\n"
            info += f"開盤價: {stock['realtime']['open']}\n"
            info += f"最高價: {stock['realtime']['high']}\n"
            info += f"最低價: {stock['realtime']['low']}\n"
            info += f"昨收價: {stock['realtime']['yesterday_close']}\n"
            
            # Convert timestamp to datetime
            timestamp = int(stock['timestamp'])  # Timestamp is already in seconds
            update_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            info += f"更新時間: {update_time}"
            
            return info
        else:
            return "無法獲取即時股票資訊。"
    except Exception as e:
        return f"發生錯誤：{str(e)}"
