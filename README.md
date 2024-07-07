# FoMOment
SITCON Hackathon 2024

## 競賽議題 & 子議題
* 團隊名稱：每周趙三餐吃蔡
* 成員姓名：周亭宇, 蔡昀潔, 趙以婷
* 競賽議題：數位心擁：資訊科技促進心理健康
  * 子議題：管理資訊，避免 FoMO X LINE

### 專案簡介
- 用途/功能：
    - 查看每日運勢、今日推薦活動
    - 整理現在的頭條新聞資訊
    - 取得股票資訊（成交價、開盤價、最低價等等）
    - 展覽資訊 **待補**
    - 跟bot聊天，抒發心情
    - 群組訊息摘要

- 目標客群&使用情境：
    - 任何有FoMO困擾的人：
      - 方便快速地取得新聞、股票、展覽、訊息摘要等資訊
      - 受每日運勢鼓勵，喝些心靈雞湯，減少無謂比較，增加充實自己的時間
      - 想找人聊天但找不到人時，可以跟FoMOment聊聊

- 操作方式：
    - 環境設置
        1. fork此專案
        2. 新增一個Line channel（messaging API），允許加入群組、webhook
        3. 新增一個Firebase realtime DB，將rules的read和write都設為true
        4. 取得Gemini API key
        5. 取得GNews API key
        6. 在Google cloud run建立服務，建構類型為Dockerfile，允許未經驗證的叫用，新增以下變數：<br>
           LINE_CHANNEL_ACCESS_TOKEN = 你的 LINE channel access token<br>
           LINE_CHANNEL_SECRET = 你的 LINE channel secret<br>
           FIREBASE_URL = 你的 Firebase realtime DB URL<br>
           GEMINI_API_KEY = 你的 Gemini API key<br>
           NEWS_API_KEY = 你的 GNews API key<br>
        7. 部署後會得到網址，將其貼在LINE channel的webhook URL
           
    - 使用者操作方式<br>
        點擊聊天室下方的選單，即可使用各種功能（群組摘要須將FoMOment加入想摘要的群組，加入後會說明使用方法）

### 使用資源
- 企業資源：
    - LINE<br>
      提供使用者服務的平台
    - GCP<br>
      部署服務的平台
    - Gemini<br>
      用於群組摘要、聊天功能
    - Firebase<br>
      用於群組摘要、每日運勢
    - GNews<br>
      用於搜尋頭條新聞
- 公開資源：
    - [政府資料開放平台](https://data.gov.tw/dataset/6012)<br>
      用於展覽資訊
    - [臺灣證券交易所 OpenAPI](https://openapi.twse.com.tw/)<br>
      用於股票資訊

### 你還想分享的事情
其實我們是第一次認真寫python的小菜雞

### 成果展示

