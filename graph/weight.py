import requests
import json
import xmltodict
import pandas as pd
import time

# API KEY
from graph.config import REST_API_KEY, OPEN_API_KEY
OPEN_API_HOST = 'http://openapi.seoul.go.kr:8088'
headers = {'Authorization': f'KakaoAK {REST_API_KEY}'}


def convert_coord():
    # vertex의 위치의 좌표계를 변경 ('input_coord': 'WTM', 'output_coord': 'WGS84')
    url = 'https://dapi.kakao.com/v2/local/geo/transcoord.json'
    df = pd.read_csv(r'data/vertex_start_end.csv')

    x_list = []
    y_list = []
    lng_list = []
    lat_list = []

    for i, row in df[['x', 'y']].drop_duplicates().iterrows():
        print(i)
        time.sleep(0.5)

        x = row['x']
        y = row['y']

        params = {'x': x, 'y': y, 'input_coord': 'WTM',
                  'output_coord': 'WGS84'}
        rep = requests.get(url, headers=headers, params=params)

        lng = rep.json()['documents'][0]['x']
        lat = rep.json()['documents'][0]['y']

        x_list.append(x)
        y_list.append(y)
        lng_list.append(lng)
        lat_list.append(lat)

        # if i % 1000 == 10:
        #     time.sleep(10)
        #     coord_df = pd.DataFrame({
        #         'x': x_list,
        #         'y': y_list,
        #         'lng': lng_list,
        #         'lat': lat_list,
        #     })
        #     coord_df.to_csv(f'data/coord_start_end_{i}.csv')

    coord_df = pd.DataFrame({
        'x': x_list,
        'y': y_list,
        'lng': lng_list,
        'lat': lat_list,
    })
    coord_df.to_csv(f'data/coord_start_end.csv')


def get_vertex():
    # 서울시 차량통행속도 csv의 LINK_ID의 vertex 정보를 저장
    edge_df = pd.read_csv(f'data/2023년 1월 서울시 차량통행속도.csv', encoding='euc-kr')

    link_id_list = []
    vertex_idx_list = []
    x_list = []
    y_list = []

    idx = 0
    for edge_id in edge_df['링크아이디'].unique():
        rep = requests.get(
            f'{OPEN_API_HOST}/{OPEN_API_KEY}/xml/LinkVerInfo/1/1000/{edge_id}')
        print(idx, len(xmltodict.parse(rep.text)['LinkVerInfo']['row']))
        idx += 1
        for i, row in enumerate(xmltodict.parse(rep.text)['LinkVerInfo']['row']):
            link_id_list.append(edge_id)
            vertex_idx_list.append(i)
            x_list.append(row['grs80tm_x'])
            y_list.append(row['grs80tm_y'])

        # if idx % 1000 == 10:
        #     time.sleep(5)
        #     vertex_df = pd.DataFrame({
        #         'LINK_ID': link_id_list,
        #         'VERTEX_IDX': vertex_idx_list,
        #         'X': x_list,
        #         'Y': y_list,
        #     })
        #     vertex_df.to_csv(f'data/vertex_{idx}.csv')

    vertex_df = pd.DataFrame({
        'LINK_ID': link_id_list,
        'VERTEX_IDX': vertex_idx_list,
        'X': x_list,
        'Y': y_list,
    })
    vertex_df.to_csv(f'data/vertex.csv')


def get_vertex_start_end():
    # LINK_ID 당 start vertex와 end vertex만 추출하여 저장
    df_vertex = pd.read_csv(f'graph/data/vertex.csv')
    df_vertex.columns = ['idx', 'LINK_ID', 'VERTEX_IDX', 'x', 'y']
    df_vertex = df_vertex[['LINK_ID', 'VERTEX_IDX', 'x', 'y']]

    df_vertex_start = df_vertex.loc[df_vertex.groupby(
        'LINK_ID').VERTEX_IDX.idxmin()]
    df_vertex_start.columns = ['LINK_ID', 'S_V', 'S_X', 'S_Y']
    df_vertex_end = df_vertex.loc[df_vertex.groupby(
        'LINK_ID').VERTEX_IDX.idxmax()]
    df_vertex_end.columns = ['LINK_ID', 'E_V', 'E_X', 'E_Y']
    df_vertex_start_end = pd.concat([df_vertex_start, df_vertex_end])
    df_vertex_start_end.to_csv(f'graph/data/vertex_start_end.csv')


def make_graph():
    df = pd.read_csv(r'data/3월 8일 차량속도.CSV', encoding='euc-kr')
    df = df[['링크아이디', '시점명', '종점명', '방향', '거리',
             '01시', '02시', '03시', '04시', '05시', '06시', '07시', '08시',
             '09시', '10시', '11시', '12시', '13시', '14시', '15시', '16시',
             '17시', '18시', '19시', '20시', '21시', '22시', '23시', '24시']]
    df.columns = ['LINK_ID', '시점명', '종점명', '방향', '거리',
                  '1시', '2시', '3시', '4시', '5시', '6시', '7시', '8시',
                  '9시', '10시', '11시', '12시', '13시', '14시', '15시', '16시',
                  '17시', '18시', '19시', '20시', '21시', '22시', '23시', '24시']
    for i in range(1, 25):
        df[f'소요시간_{i}'] = df['거리'] / (df[f'{i}시'] * 1000 / 60)

    df_vertex = pd.read_csv(f'data/vertex.csv')
    df_vertex.columns = ['idx', 'LINK_ID', 'VERTEX_IDX', 'x', 'y']
    df_vertex = df_vertex[['LINK_ID', 'VERTEX_IDX', 'x', 'y']]

    df_vertex_start = df_vertex.loc[df_vertex.groupby('LINK_ID').VERTEX_IDX.idxmin()]
    df_vertex_start.columns = ['LINK_ID', 'S_V', 'S_X', 'S_Y']
    df_vertex_end = df_vertex.loc[df_vertex.groupby('LINK_ID').VERTEX_IDX.idxmax()]
    df_vertex_end.columns = ['LINK_ID', 'E_V', 'E_X', 'E_Y']

    df_merge = pd.merge(df, df_vertex_start, on='LINK_ID')
    df_merge = pd.merge(df_merge, df_vertex_end, on='LINK_ID')

    df_coord = pd.read_csv(f'data/coord_start_end.csv')
    df_coord = df_coord[['x', 'y', 'lng', 'lat']]
    df_coord.columns = ['S_X', 'S_Y', 'S_lng', 'S_lat']
    df_merge = pd.merge(df_merge, df_coord, on=['S_X', 'S_Y'])

    df_coord.columns = ['E_X', 'E_Y', 'E_lng', 'E_lat']
    df_merge = pd.merge(df_merge, df_coord, on=['E_X', 'E_Y'])

    nodes = []
    edges = []

    # startable_node dict : check that the node is startable node
    startable_node = dict()
    ended_node = dict()

    for i, row in df_merge.iterrows():
        start_id = i * 2
        end_id = i * 2 + 1

        # marking startable node
        startable_node[start_id] = True
        ended_node[end_id] = True

        nodes.append({
            "id": start_id,
            "lat": float(row['S_lat']),
            "lng": float(row['S_lng']),
            "info": {}
        })

        nodes.append({
            "id": end_id,
            "lat": float(row['E_lat']),
            "lng": float(row['E_lng']),
            "info": {}
        })

        weight = {}

        for i in range(1, 25):
            weight[i] = int(row[f'소요시간_{i}']) if int(row[f'소요시간_{i}']) > 0 else 1

        edges.append({
            'from': start_id,
            'to': end_id,
            "info": {'id': str(row['LINK_ID']),
                     'weight': weight}
        })

    # 맨하탄 거리가 0.0002(50m) 이내라면 edge를 생성
    dist_criteria = 0.0005
    weight = {}

    for i in range(1, 25):
        weight[i] = 1

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            # nearby check
            if abs(nodes[i]['lat'] - nodes[j]['lat']) + abs(nodes[i]['lng'] - nodes[j]['lng']) < dist_criteria:
                # # Case 1 : i -> j link
                if i in startable_node and j in ended_node:
                    edges.append({
                        'from': j,
                        'to': i,
                        "info": {'id': '0000000000',
                                 'weight': weight}
                    })
                # # Case 2 : j -> i link
                if j in startable_node and i in ended_node:
                    edges.append({
                        'from': i,
                        'to': j,
                        "info": {'id': '0000000000',
                                 'weight': weight}
                    })

    logs = {"nodes": nodes,
            "edges": edges}

    # 손으로 전처리 필요
    with open('data/seoul_2.json', 'w') as f:
        json.dump(logs, f)

# 함수 순서
# get_vertex()
# get_vertex_start_end()
# convert_coord()
# make_graph()

# insert_edge_id()
