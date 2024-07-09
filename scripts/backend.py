from flask import Flask, request, jsonify, Response
import pandas as pd
import heapq
import csv
import json
from collections import defaultdict, deque

# 全局声明
graph = defaultdict(list)
stop_id_map = {}
line_id_map = {}
line_end_map = {}  # 新增：线路终点站信息
stop_to_lines = defaultdict(list)  # 新增：站点到线路的映射

def load_data():
    global graph, stop_id_map, line_id_map, line_end_map, stop_to_lines  # 使用global关键字
    stop_counter = 0
    line_counter = 0

    # 读取 bus_lines.csv 文件，存储线路终点站信息
    with open('./data/bus_lines.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            line_id = row[0]
            direction = row[2]
            end_station = row[4]
            line_dir = f"{line_id}({direction})"
            line_end_map[line_dir] = end_station

    # 读取 bus_stops.csv 文件，构建图和映射表
    with open('./data/bus_stops.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        previous_stop = {}
        for row in reader:
            line_dir = f"{row[0]}({row[1]})"
            stop_id = int(row[2])
            stop_name = row[3]

            if stop_name not in stop_id_map:
                stop_id_map[stop_name] = stop_counter
                stop_counter += 1
            if line_dir not in line_id_map:
                line_id_map[line_dir] = line_counter
                line_counter += 1

            current_stop_id = stop_id_map[stop_name]
            line_id = line_id_map[line_dir]

            # 如果当前线路的前一个站点存在，添加边
            if line_dir in previous_stop:
                prev_stop_id = previous_stop[line_dir]
                graph[prev_stop_id].append((current_stop_id, line_id))  # 添加有向边

            previous_stop[line_dir] = current_stop_id  # 更新这条线路的最后一个站点

    # 读取 stop_to_lines.csv 文件，存储站点到线路的映射
    with open('./data/stop_to_lines.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            stop_name = row[0]
            lines = row[1].split(', ')
            for line_dir in lines:
                stop_to_lines[stop_name].append(line_dir)

    return graph, stop_id_map, line_id_map, line_end_map, stop_to_lines




def bfs_shortest_path(graph, start, end):
    queue = deque([(start, 0, None)])  # (current_stop, num_stations, prev_line_id)
    visited = {start: (None, None, 0)}  # (from_stop, prev_line_id, num_stations)

    while queue:
        current, num_stations, prev_line_id = queue.popleft()

        if current == end:
            # 构建路径
            return reconstruct_path(visited, start, end)

        for neighbor, line_id in graph[current]:
            new_num_stations = num_stations + 1 if line_id != prev_line_id else num_stations
            if neighbor not in visited or visited[neighbor][2] > new_num_stations:
                visited[neighbor] = (current, line_id, new_num_stations)
                queue.append((neighbor, new_num_stations, line_id))

    return None


def format_path(path, line_id_map, stop_id_map, line_end_map):
    if not path:
        return []

    simplified_path = []
    prev_line_id = None
    num_stations = 0
    prev_from_stop = path[0][0]
    total_stations = 0

    for from_stop, to_stop, line_id in path:
        if line_id != prev_line_id:
            if prev_line_id is not None:
                from_stop_name = next(key for key, value in stop_id_map.items() if value == prev_from_stop)
                last_stop_name = next(key for key, value in stop_id_map.items() if value == from_stop)
                line_name = next(key for key, value in line_id_map.items() if value == prev_line_id)
                end_station = line_end_map[line_name]
                line_name_clean = line_name.split('(')[0]  # 去除方向数字
                simplified_path.append(f"乘坐 {line_name_clean}（{end_station}方向） 从 {from_stop_name} 到 {last_stop_name}，共 {num_stations} 站")
            prev_line_id = line_id
            num_stations = 1
            prev_from_stop = from_stop
        else:
            num_stations += 1
        total_stations += 1

    from_stop_name = next(key for key, value in stop_id_map.items() if value == prev_from_stop)
    last_stop_name = next(key for key, value in stop_id_map.items() if value == to_stop)
    line_name = next(key for key, value in line_id_map.items() if value == prev_line_id)
    end_station = line_end_map[line_name]
    line_name_clean = line_name.split('(')[0]  # 去除方向数字
    simplified_path.append(f"乘坐 {line_name_clean}（{end_station}方向） 从 {from_stop_name} 到 {last_stop_name}，共 {num_stations} 站")

    simplified_path.append(f"总站数：{total_stations}")

    return simplified_path


def reconstruct_path(visited, start, end):
    path = []
    step = end
    while step != start:
        if step in visited:
            prev, line_id, _ = visited[step]
            path.append((prev, step, line_id))
            step = prev
        else:
            return None  # 无法到达
    path.reverse()  # 反转路径
    return path

app = Flask(__name__)

@app.route('/shortest-path', methods=['POST'])
def find_shortest_path():
    data = request.json
    start_name = data['start']
    end_name = data['end']
    start = stop_id_map.get(start_name)
    end = stop_id_map.get(end_name)
    if start is None or end is None:
        return jsonify({"error": "Start or end stop not found"}), 404

    path = bfs_shortest_path(graph, start, end)
    if path:
        result = {"path": format_path(path, line_id_map, stop_id_map, line_end_map)}
        response = Response(json.dumps(result, ensure_ascii=False), content_type='application/json; charset=utf-8')
        return response
    else:
        return jsonify({"error": "No path found"}), 404
    
@app.route('/station-details', methods=['POST'])
def station_details():
    data = request.json
    station_name = data['station_name']
    lines = stop_to_lines.get(station_name)
    if not lines:
        return jsonify({"error": "Station not found or no lines available"}), 404

    line_descriptions = []
    for line_dir in lines:
        line_name = line_dir.split('(')[0]
        end_station = line_end_map[line_dir]
        line_descriptions.append(f"{line_name}（开往{end_station}）")

    result = f"{station_name}站有{len(lines)}条公交线路，分别为：" + "，".join(line_descriptions)
    response = Response(json.dumps({"details": [result]}, ensure_ascii=False), content_type='application/json; charset=utf-8')
    return response

@app.route('/search-stations', methods=['POST'])
def search_stations():
    data = request.json
    keyword = data['keyword']
    matching_stations = [station for station in stop_to_lines.keys() if keyword in station]

    if not matching_stations:
        return jsonify({"error": "No matching stations found"}), 404

    result = " ".join(matching_stations)
    response = Response(json.dumps({"stations": [result]}, ensure_ascii=False), content_type='application/json; charset=utf-8')
    return response



if __name__ == '__main__':
    load_data()  # 确保在应用启动之前加载数据
    app.run(debug=True)