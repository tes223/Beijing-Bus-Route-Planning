import gradio as gr
import requests
import json

# API URLs
API_URL = "http://localhost:5000"

def call_api(url, data):
    response = requests.post(url, json=data)
    return response.text

def format_path_result(result):
    try:
        data = json.loads(result)
        path = data.get("path", [])
        formatted_path = "\n".join(path)
        return formatted_path
    except json.JSONDecodeError:
        return result


def format_station_details(result):
    try:
        data = json.loads(result)
        details = data.get("details", [])
        
        formatted_details = ""
        for detail in details:
            formatted_detail = detail.replace("：", "：\n").replace("，", "\n")
            formatted_details += formatted_detail + "\n"
        
        return formatted_details
    except json.JSONDecodeError:
        return result
    

def format_search_stations(result):
    try:
        data = json.loads(result)
        stations = data.get("stations", [])
        formatted_stations = ""
        for station in stations:
            formatted_station = station.replace(" ", "\n")
            formatted_stations += formatted_station + "\n"
        return formatted_stations
    except json.JSONDecodeError:
        return result

def shortest_path(start, end):
    result = call_api(f"{API_URL}/shortest-path", {'start': start, 'end': end})
    return format_path_result(result)

def station_details(station_name):
    result = call_api(f"{API_URL}/station-details", {'station_name': station_name})
    return format_station_details(result)

def search_stations(keyword):
    result = call_api(f"{API_URL}/search-stations", {'keyword': keyword})
    return format_search_stations(result)

with gr.Blocks() as app:
    with gr.Tab("最短路径查询"):
        start_input = gr.Textbox(label="起始站点")
        end_input = gr.Textbox(label="到达站点")
        output_path = gr.Textbox(label="最短路径信息", lines=10)
        btn_path = gr.Button("查询")
        btn_path.click(shortest_path, inputs=[start_input, end_input], outputs=output_path)
        gr.Markdown("""
        ## 
        - 请输入起始站点和到达站点名称。如不确定站名，请在“关键字搜索”功能中进行模糊搜索。
        - 输入站名后点击“查询”按钮，即可获取从起始站点到到达站点的最短路径信息。此最短路径是在站数上最短，并非物理最短。
        - 本程序使用的数据源较为老旧，现有公交线路存在很大变化，请勿在实际生活中使用本软件进行线路规划。
        """)

    with gr.Tab("站点详细信息查询"):
        station_input = gr.Textbox(label="站点名称")
        output_info = gr.Textbox(label="站点详细信息", lines=10)
        btn_info = gr.Button("查询")
        btn_info.click(station_details, inputs=[station_input], outputs=output_info)
        gr.Markdown("""
        ## 
        - 输入想要查询的站点名称。如不确定站名，请在“关键字搜索”功能中进行模糊搜索。
        - 点击“查询”按钮，获取该站点的详细信息。
        - 本程序使用的数据源较为老旧，现有公交线路存在很大变化，请勿在实际生活中使用本软件进行信息查询。
        """)

    with gr.Tab("关键字搜索"):
        keyword_input = gr.Textbox(label="关键字")
        output_search = gr.Textbox(label="搜索结果", lines=10)
        btn_search = gr.Button("搜索")
        btn_search.click(search_stations, inputs=[keyword_input], outputs=output_search)
        gr.Markdown("""
        ## 
        - 输入关键字，用于搜索站点名称中包含该关键字的所有站点。
        - 点击“搜索”按钮，显示所有相关站点名称。
        - 本程序使用的数据源较为老旧，现有公交线路存在很大变化，很多站点存在更名，新增或撤销，请以北京公交/一路同行app中的最新信息为准。
        """)


    with gr.Tab("说明"):
        gr.Markdown("""
        ## 一些作者想要说的话

        **关于环境配置**
        - 你已经看到这个页面了，其实多半已经成功部署了！如果在使用或部署中遇到任何问题，记得关注控制台的错误信息，会带你找到问题的解决方案。

        **关于使用问题**
        - 如果你点击确定后好长时间窗口没有任何反应（甚至没有加载中页面），那多半是站名输的有问题，请前往站名搜索标签，搜索正确的站名，再查找路线。
        - 本程序认为所有车站的站间距都是一样的，所以这里给出的最短路径并不是实际乘车的最短路径。再加上北京公交快车大站距的实际情况，使用本软件进行乘车规划会导致绕路！再加上北京公交官网数据更新不及时的实际情况，请勿将本程序应用于实际乘车！乘车规划路线请使用一路同行APP或者高德百度等靠谱的地图软件！
        - 如果前端莫名其妙连不上后端，请检查是不是挂了梯子，如果是的话，把梯子关掉。
                    
        **版权声明**
        - 本程序由github用户"tes223"设计并编写，其中站点信息获取时的逻辑参考了github用户"CakeAL"的代码（已获得本人同意），其余代码均为本人编写。
        - 请勿将本程序直接当做作业上交，要交作业的话，你至少应该把这部分版权声明删了。但凡你会一点python的话，只要稍微看懂一点本项目的代码逻辑，删掉这部分版权声明非常简单。
                    
        **联系作者**
        - contact me at xingjuustb@foxmail.com

        """)

app.launch()
