import requests
import os
import json
import re
import datetime

def getTime(appKey):
    url = os.environ.get("APIURL")
    year_str = str(datetime.date.today().year)
    requestParams = {
        'key': appKey,
        'year': year_str,
        'name': '',
    }
    response = requests.get(url, params=requestParams)

    # 解析响应结果
    if response.status_code == 200:
        return response.json()
    else:
        # 网络异常等因素，解析结果异常。可依据业务逻辑自行处理。
        print('请求异常')
        return None

def json_to_ics_array(data):
    result = []

    for item in data.get("result", []):
        name = item.get("name", "").strip()

        # 读取年份
        year_str = item.get("pub_year", "").strip()
        if not year_str.isdigit():
            continue
        year = int(year_str)

        # 提取月份和日期
        date_match = re.match(r"(\d+)月(\d+)日", item.get("pub_date", ""))
        if not date_match:
            continue
        month = int(date_match.group(1))
        day = int(date_match.group(2))

        # 提取时间
        time_parts = item.get("pub_time", "00:00:00").split(":")
        if len(time_parts) != 3:
            continue
        hour, minute, second = map(lambda x: f"{int(x):02d}", time_parts)

        # 拼接时间格式 YYYYMMDDTHHMMSS
        dt_str = f"{year:04d}{month:02d}{day:02d}T{hour}{minute}{second}"

        result.append([name, dt_str])

    return result

def generate_ics_from_array(pairs, output_path='ics-files/SolarTermsDateAndTime.ics'):
    header = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//IOS Solar Terms Supplement//Solar Terms Calendar//CN
CALSCALE:GREGORIAN
X-WR-CALNAME:节气补充
X-WR-CALDESC:对IOS日历的节气日历和时间点进行补充
X-WR-TIMEZONE:Asia/Shanghai

"""

    footer = "END:VCALENDAR\n"

    events = []
    for idx, (name, dt_str) in enumerate(pairs, 1):
        event = f"""\
BEGIN:VEVENT
UID:{idx}@solar_term.cn
SUMMARY:{name}
DTSTART;TZID=Asia/Shanghai:{dt_str}
BEGIN:VALARM
TRIGGER:-PT0M
ACTION:DISPLAY
END:VALARM
END:VEVENT"""
        events.append(event)

    # 拼接，事件之间用一个换行分隔，开头header直接跟第一个事件之间没有多余空行
    content = header + "\n\n".join(events) + "\n" + footer

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ 生成成功：{output_path}")

if __name__ == '__main__':
    appKey = os.environ.get("APPKEY")
    arr = json_to_ics_array(getTime(appKey))
    generate_ics_from_array(arr)
    print("完成！")

