import networkx as nx
import os
from tqdm import tqdm

from map import get_map, update_weight


# file path setting
cwd = os.path.abspath(os.path.dirname(__file__))

graph_name = '20230426_seoul_default_0_7_st_link'

node, node_idx, graph = get_map(graph_name)

for hour in range(1, 24):
    print(f"{hour} distance calc start")
    update_weight(graph_name, hour)
    print(f"{hour} distance calc end")

    file_path = os.path.join(cwd, f'data/dist_20230426_seoul_default_0_7_st_link_{hour}.csv')

    with open(file_path, "w") as file:
        for i in tqdm(range(len(node))):
            my_dict = nx.single_source_dijkstra_path_length(graph, i, weight='weight')
            sorted_items = sorted(my_dict.items(), key=lambda x: x[0])
            result = ','.join([f"{value:.2f}" for key, value in sorted_items])
            file.write(result + '\n')
