import pandas as pd
import networkx as nx

from graph.route import get_map, update_weight
import seaborn as sns
import matplotlib.pyplot as plt

# 서울시 맵 default weight를 0.1로 link 연결 했다는 의미
graph_name = 'seoul_default_0_1_link'
nodes, node_idx, graph = get_map(graph_name)

df_task = pd.read_csv('data/reqeust_200108.csv')
df_task['req_hour'] = df_task['req_time'].map(lambda x: int(x.split(":")[0]))
df_task['move_time'] = pd.to_datetime(df_task['end_time']) - pd.to_datetime(df_task['start_time'])

move_time = []
real_move_time = []
time_diff = []
time_diff_percent = []

for h in range(0, 24):
    df_task_h = df_task[df_task['req_hour'] == h]
    update_weight(graph_name, h % 24 + 1)

    for i, row in df_task_h.iterrows():
        move_unload_time = nx.shortest_path_length(graph, row['start_node'], row['end_node'], weight='weight')
        real_move_unload_time = ((row['move_time'].total_seconds() / 60) + 1440) % 1440
        move_time.append(move_unload_time)
        real_move_time.append(real_move_unload_time)
        time_diff.append(move_unload_time - real_move_unload_time)
        time_diff_percent.append((move_unload_time - real_move_unload_time) / real_move_unload_time * 100)

plt.figure(figsize=(8, 4))
sns.histplot(data=move_time)
plt.savefig("img/move_time.png")

plt.figure(figsize=(8, 4))
sns.histplot(data=real_move_time)
plt.savefig("img/real_move_time.png")

plt.figure(figsize=(8, 4))
sns.histplot(data=time_diff)
plt.savefig("img/time_diff.png")

plt.figure(figsize=(8, 4))
sns.histplot(data=time_diff_percent)
plt.savefig("img/time_diff_percent.png")
