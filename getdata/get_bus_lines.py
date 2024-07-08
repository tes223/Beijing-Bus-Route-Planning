import requests
import re
import csv

# 北京公交主页，用于获取全部线路名称
MAIN_URL = r"https://www.bjbus.com/home/index.php"
AJAX_RTBUS_DATA = r"https://www.bjbus.com/home/ajax_rtbus_data.php"

def get_all_line_number():
    r = requests.get(MAIN_URL)
    return re.findall('<a href="javascript:;">(.*?)</a>', r.content.decode(encoding="utf-8"))

def get_lines_with_directions(all_line_number):
    with open('../data/bus_lines.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for line in all_line_number:
            r = requests.get(AJAX_RTBUS_DATA, params={"act": "getLineDir", "selBLine": line})
            pattern = r'<a href="javascript:;" data-uuid="(\d+)">(.*?)\((.*?)-(.*?)\)</a>'
            matches = re.findall(pattern, r.content.decode(encoding="utf-8"))
            results = [
                (matches[i][1], matches[i][0], i, matches[i][2], matches[i][3])
                for i in range(0, len(matches))
            ]
            for line_data in results:
                writer.writerow(line_data)
                print(line_data[0] + " 方向: " + str(line_data[2]) + " 存储完成")

def main():
    all_line_number = get_all_line_number()
    get_lines_with_directions(all_line_number)

if __name__ == "__main__":
    main()
