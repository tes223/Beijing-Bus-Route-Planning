import chardet
import codecs
import pandas as pd
import os

# 输入文件的编码类型
encode_in = 'gb18030'

# 输出文件的编码类型
encode_out = 'utf-8'

with codecs.open(filename="../data/bus_lines.csv", mode='r', encoding=encode_in) as fi:
    data = fi.read()
    with open("../data/bus_lines_utf8.csv", mode='w', encoding=encode_out) as fo:
        fo.write(data)
        fo.close()

with open("../data/bus_lines_utf8.csv", 'rb') as f:
    data = f.read()
    print(chardet.detect(data))
    

with codecs.open(filename="../data/bus_stops.csv", mode='r', encoding=encode_in) as fi:
    data = fi.read()
    with open("../data/bus_stops_utf8.csv", mode='w', encoding=encode_out) as fo:
        fo.write(data)
        fo.close()

with open("../data/bus_stops_utf8.csv", 'rb') as f:
    data = f.read()
    print(chardet.detect(data))


with codecs.open(filename="../data/stop_to_lines.csv", mode='r', encoding=encode_in) as fi:
    data = fi.read()
    with open("../data/stop_to_lines_utf8.csv", mode='w', encoding=encode_out) as fo:
        fo.write(data)
        fo.close()

with open("../data/stop_to_lines_utf8.csv", 'rb') as f:
    data = f.read()
    print(chardet.detect(data))

os.remove("../data/bus_lines.csv")
os.remove("../data/bus_stops.csv")
os.remove("../data/stop_to_lines.csv")
os.rename("../data/bus_lines_utf8.csv", "../data/bus_lines.csv")
os.rename("../data/bus_stops_utf8.csv", "../data/bus_stops.csv")
os.rename("../data/stop_to_lines_utf8.csv", "../data/stop_to_lines.csv")

dataFrame = pd.read_csv("../data/bus_lines.csv")
dataFrame = dataFrame.dropna()
dataFrame.to_csv("../data/bus_lines.csv", index=False)

dataFrame = pd.read_csv("../data/bus_stops.csv")
dataFrame = dataFrame.dropna()
dataFrame.to_csv("../data/bus_stops.csv", index=False)

dataFrame = pd.read_csv("../data/stop_to_lines.csv")
dataFrame = dataFrame.dropna()
dataFrame.to_csv("../data/stop_to_lines.csv", index=False)