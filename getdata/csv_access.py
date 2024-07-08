import csv

def get_csv_file(file_path, mode='r'):
    return open(file_path, mode, newline='')

def create_bus_number_table():
    with get_csv_file("../data/bus_lines.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["线路号", "data_uuid", "方向", "始发站", "终到站"])

def insert_to_bus_number(data):
    with get_csv_file("../data/bus_lines.csv", 'a') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def create_stops_table():
    with get_csv_file("../data/stops.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["线路号", "方向", "站编号", "站名"])

def insert_to_stops(data):
    with get_csv_file("../data/stops.csv", 'a') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def get_all_lines():
    data = []
    with get_csv_file("../data/bus_lines.csv") as file:
        reader = csv.reader(file)
        for line_info in reader:
            data.append(line_info)
    return data

def create_stop_to_lines_table():
    with get_csv_file("../data/stop_to_lines.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["站名", "线路"])

def reset_data_to_stop_to_lines():
    stops = set()
    with get_csv_file("../data/bus_stops.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            stops.add(row[3])

    with get_csv_file("../data/stop_to_lines.csv", 'a') as file:
        writer = csv.writer(file)
        for stop in stops:
            with get_csv_file("../data/bus_stops.csv") as stops_file:
                stops_reader = csv.reader(stops_file)
                routes_data = [(row[0], row[1]) for row in stops_reader if row[3] == stop]
                routes_str = ", ".join([f"{route[0]}({route[1]})" for route in routes_data])
                writer.writerow([stop, routes_str])
    print("完成整理数据到stop_to_lines表中")

def main():
    # create_bus_number_table()
    # insert_to_bus_number(data)
    # create_stops_table()
    # get_all_lines()
    # create_stop_to_lines_table()
    reset_data_to_stop_to_lines()
    _ = 123

if __name__ == "__main__":
    main()
