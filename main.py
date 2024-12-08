'''
from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

# 加載時刻表資料
df1 = pd.read_excel('thsrc_timetable_cleaned.xlsx')  # 北上
df2 = pd.read_excel('thsrc_timetable_cleaned.xlsx')  # 南下
df1.replace('─', np.nan, inplace=True)
df2.replace('─', np.nan, inplace=True)

# 車站對應表
stations = {
    '左營': 1, '台南': 2, '嘉義': 3, '雲林': 4, '彰化': 5, '台中': 6,
    '苗栗': 7, '新竹': 8, '桃園': 9, '板橋': 10, '台北': 11, '南港': 12
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/getSchedule', methods=['POST'])
def get_schedule():
    data = request.json
    start = data.get('start')
    arrive = data.get('arrive')
    time = data.get('time')

    if not start or not arrive or not time:
        return jsonify({'error': '缺少必要參數'}), 400

    # 轉換時間格式
    hour, minute = map(int, time.split(":"))
    time_in_minutes = hour * 60 + minute

    # 確定方向
    start_idx = stations[start]
    arrive_idx = stations[arrive]
    direction = "北上" if arrive_idx > start_idx else "南下"
    df = df1 if direction == "北上" else df2

    # 查詢符合條件的車次
    results = []
    for _, row in df.iterrows():
        departure_time = row[start_idx + 1]
        arrival_time = row[arrive_idx + 1]
        if pd.isna(departure_time) or pd.isna(arrival_time):
            continue

        dep_hour, dep_minute = map(int, departure_time.split(":"))
        dep_time_in_minutes = dep_hour * 60 + dep_minute

        if dep_time_in_minutes >= time_in_minutes:
            results.append({
                'departure': departure_time,
                'arrival': arrival_time,
            })

    return jsonify(results if results else {'message': '沒有符合條件的車次'})

if __name__ == '__main__':
    app.run(debug=True)
    '''
from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

# 加載時刻表資料
df1 = pd.read_excel('thsrc_timetable_north.xlsx')  # 北上
df2 = pd.read_excel('thsrc_timetable_south.xlsx')  # 南下
df1.replace('─', np.nan, inplace=True)
df2.replace('─', np.nan, inplace=True)

# 車站對應表
stations = {
    '左營': 1, '台南': 2, '嘉義': 3, '雲林': 4, '彰化': 5, '台中': 6,
    '苗栗': 7, '新竹': 8, '桃園': 9, '板橋': 10, '台北': 11, '南港': 12
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/getSchedule', methods=['POST'])
def get_schedule():
    data = request.json
    start = data.get('start')
    arrive = data.get('arrive')
    time = data.get('time')

    if not start or not arrive or not time:
        return jsonify({'error': '缺少必要參數'}), 400

    # 轉換時間格式
    hour, minute = map(int, time.split(":"))
    time_in_minutes = hour * 60 + minute

    # 確定方向
    start_idx = stations[start]
    arrive_idx = stations[arrive]
    direction = "北上" if arrive_idx > start_idx else "南下"
    df = df1 if direction == "北上" else df2

    # 查詢符合條件的車次
    results = []
    for _, row in df.iterrows():
        departure_time = row[start_idx + 1]
        arrival_time = row[arrive_idx + 1]
        if pd.isna(departure_time) or pd.isna(arrival_time):
            continue

        dep_hour, dep_minute = map(int, departure_time.split(":"))
        dep_time_in_minutes = dep_hour * 60 + dep_minute

        if dep_time_in_minutes >= time_in_minutes:
            results.append({
                'departure': departure_time,
                'arrival': arrival_time,
            })

    return jsonify(results if results else {'message': '沒有符合條件的車次'})

if __name__ == '__main__':
    app.run(debug=True)