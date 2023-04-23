import json
from collections import deque
from tqdm import tqdm

weight = {}
DEFAULT_WEIGHT: float = 0.5

for i in range(1, 25):
    weight[i] = DEFAULT_WEIGHT


class Linker:
    """
    ## Parameter
    readFilePath : origin file
    writeFilePath : linked file
    mainNode : find main graph with mainNode
    ## Case define
    ### Case 0.
    can 0 Node -> target Node
    ### Case 1.
    can not 0 Node -> target Node
    ### Case 2.
    Can target Node -> 0 Node
    ### Case 3.
    Can not target Node -> 0 Node
    ***
    ## Solution
    ### step 1.
    find case 0 node, case 1 node
    ### step 2.
    liking and change case 1 -> case 0
    - there is no Case 1 node, so we have just case 2 Node
    ### step 3.
    find case 2, case 3 node
    ### step 4.
    linking and change case 3 -> case 2
    """

    CASE1_EDGE_ID: str = '2000000000'
    CASE3_EDGE_ID: str = '3000000000'

    def __init__(self, readFilePath: str, writeFilePath: str, mainNode: int):

        self.readFilePath = readFilePath
        self.writeFilePath = writeFilePath
        self.mainNode = mainNode

        self.nodes_list = []
        self.edges_list = []

        self.nodes = dict()
        self.edges = dict()
        self.startable_node = dict()
        self.ended_node = dict()
        self.Case_0 = dict()
        self.Case_1 = dict()
        self.Case_2 = dict()
        self.Case_3 = dict()

    def readFile(self, filePath: str):
        # file open and make list , list is origin data
        with open(filePath, 'r') as file:
            logs = json.load(file)
        self.nodes_list = logs['nodes']
        self.edges_list = logs['edges']

    def updateDict(self):
        """
        update node and edges dict :
        list -> dict
        """

        self.nodes = dict()
        self.edges = dict()
        self.startable_node = dict()
        self.ended_node = dict()

        for n in self.nodes_list:
            self.nodes[n['id']] = {'lat': n['lat'],
                                   'lng': n['lng'], 'linked': [], 'edgeid': []}

        for e in self.edges_list:
            self.edges[e['info']['id']] = {'from': e['from'], 'to': e['to']}
            self.nodes[e['from']]['linked'].append(e['to'])
            self.nodes[e['from']]['edgeid'].append(e['info']['id'])

            # marking startable node
            self.startable_node[e['from']] = True
            self.ended_node[e['to']] = True

    def findCase0(self):
        """
        Find Case 0,
        update Case 0 dict
        """

        self.Case_0 = dict()
        que = deque([])

        # insert firstNode node and start
        que.append(self.mainNode)
        cur_node = self.mainNode

        while len(que) > 0:
            cur_node = que.popleft()
            if self.Case_0.get(cur_node) != None:
                continue
            for i in self.nodes[cur_node]['linked']:
                que.append(i)
            self.Case_0[cur_node] = True

        print(
            f"[CASE 0] linked Node count from {self.mainNode} Node : {str(len(self.Case_0))}")

    def findCase1(self):
        """
        Find Case 1
        update Case 1 dict
        """
        self.Case_1 = dict()
        for i in self.nodes:
            if self.Case_0.get(i) == None:
                self.Case_1[i] = True

        print(
            f"[CASE 1] linked Node count from {self.mainNode} Node : {str(len(self.Case_1))}")

    def convertCase1to0(self):

        # find Case 0, Case 1
        self.findCase0()
        self.findCase1()

        # change case 1 -> case 0 : link case 0 node -> case 1 node
        print("[CONVERT] Processing Convert Case 1 to Case 0")

        for c1 in tqdm(self.Case_1):
            nearby_node = -1
            shortest_distance = 10000000
            for c0 in self.Case_0:
                distance = abs(self.nodes[c1]['lat'] - self.nodes[c0]['lat']) + \
                    abs(self.nodes[c1]['lng'] - self.nodes[c0]['lng'])
                if distance < shortest_distance:
                    shortest_distance = distance
                    nearby_node = c0

            if nearby_node == -1:
                print("[ERROR] can not find shortest node!")

            self.edges_list.append({
                'from': nearby_node,
                'to': c1,
                "info": {'id': self.CASE1_EDGE_ID,
                         'weight': weight}
            })

        self.updateDict()
        print("[CONVERT] Complete convert Case 1 to Case 0")

        # Check Case 0, Case 1
        self.findCase0()
        self.findCase1()

    def findCase2(self):
        """
        Find Case 2 Node
        """

        self.Case_2 = dict()
        for n in self.Case_0:
            self.Case_2[n] = False

        print("[Case 2] find Case 2 Node processing...")

        # looping linked n node and
        for n in tqdm(self.Case_0):
            visited = dict()
            que = deque([])
            n_break = False

            que.append(n)
            cur_node = n

            while len(que) > 0 and n_break == False:
                cur_node = que.popleft()
                if visited.get(cur_node) != None:
                    continue
                for i in self.nodes[cur_node]['linked']:
                    if i == 0:
                        n_break = True
                        self.Case_2[n] = True
                        break
                    que.append(i)
                visited[cur_node] = True

        print(
            f"[Case 2] Comeback to {self.mainNode} node count : {len(self.Case_2)}")

    def findCase3(self):

        self.Case_3 = dict()
        for i in self.Case_2:
            if self.Case_2[i] == False:
                self.Case_3[i] = True

        for i in self.Case_3:
            self.Case_2.pop(i)

        print(
            f"[Case 3] Can not Comeback to {self.mainNode} node count : {len(self.Case_3)}")

    def convertCase3to2(self):

        # find case 2, 3
        self.findCase2()
        self.findCase3()

        # change case 3 -> case 2 : link case 3 node -> case 2 node
        print("[CONVERT] Processing Convert Case 3 to Case 2")
        for c3 in self.Case_3:

            nearby_node = -1
            shortest_distance = 10000000
            for c2 in self.Case_2:
                distance = abs(self.nodes[c3]['lat'] - self.nodes[c2]['lat']) + \
                    abs(self.nodes[c3]['lng'] - self.nodes[c2]['lng'])
                if distance < shortest_distance:
                    shortest_distance = distance
                    nearby_node = c2

            if nearby_node == -1:
                print("[ERROR] can not find shortest node!")

            self.edges_list.append({
                'from': c3,
                'to': nearby_node,
                "info": {'id': self.CASE3_EDGE_ID,
                         'weight': weight}
            })

        self.updateDict()
        print("[CONVERT] Complete convert Case 3 to Case 2")

        # check case 2, 3
        self.findCase2()
        self.findCase3()

    def checkAllNodeLink(self):
        """
        Check All Node linkied status.
        method : all node's case 0 count == node's count
        """

        print("Checking All Node Linked...")
        for cur_node in tqdm(self.nodes):
            visited = dict()
            que = deque([])

            que.append(cur_node)
            cur_node = cur_node

            while len(que) > 0:
                cur_node = que.popleft()
                if visited.get(cur_node) != None:
                    continue
                for i in self.nodes[cur_node]['linked']:
                    que.append(i)
                visited[cur_node] = True

            if len(visited) != len(self.nodes):
                print(f"{cur_node} is not linked all node!")
                break

    def writeFile(self):
        result = {"nodes": self.nodes_list,
                  "edges": self.edges_list}

        # 손으로 전처리 필요
        with open(self.writeFilePath, 'w') as f:
            json.dump(result, f)

    def processing(self):
        self.readFile(self.readFilePath)
        self.updateDict()
        self.convertCase1to0()
        self.convertCase3to2()
        self.checkAllNodeLink()
        self.writeFile()


if __name__ == "__main__":
    linker = Linker('./data/seoul_j.json',
                    './data/seoul_link_j.json', 0)
    linker.processing()
