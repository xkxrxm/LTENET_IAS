from io import BytesIO

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from utils.token import validate_token
from .pylouvain import PyLouvain, in_order
import pandas as pd
from matplotlib import pyplot as plt
import networkx as nx

router = APIRouter(
    tags=["网络干扰结构分析"]
)


def get_pos():
    csv_data = pd.read_csv(r"D:/BaiduSyncdisk/PythonWorkplace/LTENET_IAS/interStruAnalysis/tbcell.csv", encoding='utf-8', usecols=['SECTOR_ID', 'LONGITUDE', 'LATITUDE'])
    coordinate_dict = {}
    for index, row in csv_data.iterrows():
        coordinate_dict[str(row['SECTOR_ID'])] = [row['LONGITUDE'], row['LATITUDE']]
    return coordinate_dict


@router.get('/graph')
async def get_graph():
    filepath = 'D:/BaiduSyncdisk/PythonWorkplace/LTENET_IAS/interStruAnalysis/tbC2I.txt'  # 获取社区划分
    # pyl = PyLouvain.from_file(filepath)
    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()
    nodes = {}
    edges = []
    for line in lines:
        n = line.split()
        if not n:
            break
        nodes[n[0]] = 1
        nodes[n[1]] = 1
        w = 1
        if len(n) == 3:
            w = float(n[2])
        edges.append(((n[0], n[1]), w))
    # rebuild graph with successive identifiers
    nodes_, edges_ = in_order(nodes, edges)
    # print("%d nodes, %d edges" % (len(nodes_), len(edges_)))
    pyl = PyLouvain(nodes_, edges_)

    node_dict = dict(zip(nodes.keys(), nodes_))  # key 是 253916-2 的形式，value 是编号的形式
    reverse_node_dict = dict(zip(node_dict.values(), node_dict.keys()))  # key 是编号的形式，value是 253916-2 的形式
    partition, q = pyl.apply_method()
    # print(partition)
    # print("模块度：", q)

    # 给各个社区节点分配颜色
    community_num = len(partition)
    # print('community_num:', community_num)
    color_board = ['red', 'green', 'blue', 'pink', 'orange', 'purple', 'scarlet']
    color = {}
    for index in range(community_num):
        # print("社区" + str(index + 1) + ":" + str(len(partition[index])))
        for node_id in partition[index]:
            color[node_id] = color_board[index]  # color 为一个字典，key 为编号形式的节点，value 为所属社区的颜色
    new_color_dict = sorted(color.items(), key=lambda d: d[0], reverse=False)  # 将 color 字典按照 key 的大小排序，并返回一个 list
    node_list = [reverse_node_dict[item[0]] for item in new_color_dict]  # 存储编号从小到大顺序对应的 253916-2 的形式的节点
    color_list = [item[1] for item in new_color_dict]  # 存储 node_list 中对应的节点颜色
    # print(node_list)
    # print(color_list)

    # 构建 networkx 无向图
    G = nx.Graph()
    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()
    edge_list = []  # 存储边列表
    edge_width = []  # 存储边列表对应的边粗细
    edge_color = []  # 存储边列表对应的边颜色
    for line in lines:
        n = line.split()
        if not n:
            break
        G.add_edge(n[0], n[1], weight=float(n[2]))
        edge_list.append([n[0], n[1]])
        if color[node_dict[n[0]]] == color[node_dict[n[1]]]:  # 如果边的两端颜色相同
            edge_color.append(color[node_dict[n[0]]])  # 则使用点的颜色作为边的颜色
        else:
            edge_color.append('c')  # 否则使用其他颜色
        if float(n[2]) > 0:  # 阈值
            edge_width.append(float(n[2]) / 100.0)
        else:
            edge_width.append(0.0)

    # 可视化
    plt.figure(figsize=(50, 50))
    pos_dict = get_pos()
    _node = [int(item.split("-")[-1]) % 4 for item in node_list]  # 提取后缀模 4 取余
    node_0_index_list, node_1_index_list, node_2_index_list, node_3_index_list = [], [], [], []
    for index, item in enumerate(_node):  # 划分不同后缀余数的群，以便给每个群分配一个节点的形状 node_shape 防止都用圆形，导致同一经纬度的节点重叠在一起
        if item == 0:
            node_0_index_list.append(index)
        if item == 1:
            node_1_index_list.append(index)
        if item == 2:
            node_2_index_list.append(index)
        if item == 3:
            node_3_index_list.append(index)
    # print("node_list:", _node)
    nx.draw_networkx_nodes(G, pos_dict, nodelist=[node_list[i] for i in node_0_index_list], node_shape=7,
                           node_color=[color_list[i] for i in node_0_index_list], node_size=50)
    nx.draw_networkx_nodes(G, pos_dict, nodelist=[node_list[i] for i in node_1_index_list], node_shape=4,
                           node_color=[color_list[i] for i in node_1_index_list], node_size=50)
    nx.draw_networkx_nodes(G, pos_dict, nodelist=[node_list[i] for i in node_2_index_list], node_shape=5,
                           node_color=[color_list[i] for i in node_2_index_list], node_size=50)
    nx.draw_networkx_nodes(G, pos_dict, nodelist=[node_list[i] for i in node_3_index_list], node_shape=6,
                           node_color=[color_list[i] for i in node_3_index_list], node_size=50)
    nx.draw_networkx_edges(G, pos_dict, edgelist=edge_list, width=edge_width, alpha=1, edge_color=edge_color)
    buf = BytesIO()
    plt.savefig(buf, format="jpeg")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/jpeg")
