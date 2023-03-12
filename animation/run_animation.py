import pygame
import json
import random

from route.route import get_graph

BLOCK_SIZE = 1700
TASK_SIZE = 10

VEHICLE_COLOR = {
    0: (255, 0, 0),  # WAIT
    1: (195, 0, 0),  # ALLOC
    2: (195, 0, 0),  # MOVE_TO_LOAD
    3: (165, 0, 0),  # LOAD_START
    4: (165, 0, 0),  # LOADING
    5: (165, 0, 0),  # LOAD_END
    6: (105, 0, 0),  # MOVE_TO_UNLOAD
    7: (75, 0, 0),  # UNLOAD_START
    8: (75, 0, 0),  # UNLOADING
    9: (75, 0, 0),  # UNLOAD_END
}

ROAD_COLOR = {
    1: (0, 255, 0),
    2: (255, 212, 0),
    3: (238, 85, 19),
    4: (210, 24, 24),
}


TASK_COLOR = {}

tax_img = pygame.image.load('taxi.jpg')
tax_img = pygame.transform.scale(tax_img, (10, 10))


def draw_road(surface, node, graph):
    for edge in graph.edges():
        weight = graph.get_edge_data(edge[0], edge[1])['weight']

        pygame.draw.line(surface, ROAD_COLOR[weight],
                         ((node[edge[0]][1] - MIN[1]) * BLOCK_SIZE, 500 - (node[edge[0]][0] - MIN[0]) * BLOCK_SIZE),
                         ((node[edge[1]][1] - MIN[1]) * BLOCK_SIZE, 500 - (node[edge[1]][0] - MIN[0]) * BLOCK_SIZE))


def read_log(log_path):
    with open(log_path, 'r') as file:
        logs = json.load(file)

    return logs['logs']


def draw_vehicle(surface, loc):
    surface.blit(tax_img, ((loc[1] - MIN[1]) * BLOCK_SIZE, 500 - (loc[0] - MIN[0]) * BLOCK_SIZE))


def draw_vehicles(surface, vehicles):
    for vehicle in vehicles:
        loc = (vehicle['lat'], vehicle['lng'])

        draw_vehicle(surface, loc)


def draw_load_task(surface, t_idx, loc):
    loc = ((loc[1] - MIN[1]) * BLOCK_SIZE, 500 - (loc[0] - MIN[0]) * BLOCK_SIZE)
    pygame.draw.circle(surface, TASK_COLOR[t_idx % 100], loc, TASK_SIZE / 2)


def draw_unload_task(surface, t_idx, loc):
    loc = ((loc[1] - MIN[1]) * BLOCK_SIZE, 500 - (loc[0] - MIN[0]) * BLOCK_SIZE)
    pygame.draw.circle(surface, TASK_COLOR[t_idx % 100], loc, TASK_SIZE / 2, 3)


def draw_tasks(surface, tasks):
    for task in tasks:
        t_idx = task['id']
        status = task['status']
        if 0 <= status <= 4:
            draw_load_task(surface, t_idx, (task['pick_lat'], task['pick_lng']))
            draw_unload_task(surface, t_idx, (task['drop_lat'], task['drop_lng']))
        elif 5 <= status <= 8:
            draw_unload_task(surface, t_idx, (task['drop_lat'], task['drop_lng']))
        elif status == 9:
            continue
        else:
            print("Error")


def set_task_color():
    random.seed(0)
    for i in range(100):
        TASK_COLOR[i] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))


logs = read_log("../log/20230312_214850.json")
node, node_idx, graph = get_graph('seoul_gu')

MIN = [9999, 9999]
for n in node:
    MIN[0] = min(MIN[0], node[n][0])
    MIN[1] = min(MIN[1], node[n][1])

set_task_color()

pygame.init()
screen = pygame.display.set_mode((500, 500))

log_idx = 0

while True:
    log = logs[log_idx]
    n_time = log['time']
    vehicles = log['vehicles']
    tasks = log['tasks']

    screen.fill((0, 0, 0))

    draw_road(screen, node, graph)
    draw_tasks(screen, tasks)
    draw_vehicles(screen, vehicles)

    if pygame.event.get(pygame.QUIT):
        break

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and log_idx > 0:
                log_idx -= 1
            if event.key == pygame.K_RIGHT and log_idx < len(logs) - 1:
                log_idx += 1

    pygame.display.update()

pygame.quit()
