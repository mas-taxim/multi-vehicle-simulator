import networkx as nx
import os

from graph.map import get_map, update_weight

graph_name = '20230426_seoul_default_0_7_st_link'

node, node_idx, graph = get_map(graph_name)

for hour in range(12, 25):
    print(hour)
    update_weight(graph_name, hour)

    file_path = f"dist_20230426_seoul_default_0_7_st_link_{hour}.csv"  # 저장할 파일 경로

    with open(file_path, "w") as file:
        for i in range(len(node)):
            my_dict = nx.single_source_dijkstra_path_length(graph, i, weight='weight')
            sorted_items = sorted(my_dict.items(), key=lambda x: x[0])
            result = ','.join([f"{value:.2f}" for key, value in sorted_items])
            file.write(result + '\n')

