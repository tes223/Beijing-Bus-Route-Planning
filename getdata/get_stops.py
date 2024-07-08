import requests
import re
import csv

# 导入写入和读取CSV文件的函数
from csv_access import insert_to_stops, get_all_lines

AJAX_RTBUS_DATA = r"https://www.bjbus.com/home/ajax_rtbus_data.php"

def get_stops(line_id, data_uuid, direction):
    r = requests.get(
        AJAX_RTBUS_DATA,
        params={"act": "getDirStation", "selBLine": line_id, "selBDir": data_uuid},
    )
    pattern = r'<a href="javascript:;" data-seq="(\d+)">(.*?)</a>'
    matches = re.findall(pattern, r.content.decode(encoding="utf-8"))
    results = [(line_id, direction, int(match[0]), match[1]) for match in matches]
    return results

def main():
    all_line = get_all_lines()
    with open('../data/bus_stops.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for line in all_line:
            results = get_stops(line[0], line[1], line[2])
            for res in results:
                writer.writerow(res)
                print(line[0] + " 方向: " + str(line[2]) + " 站点存储完成")

if __name__ == "__main__":
    main()
