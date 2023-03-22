import importer  # resolve releative import path
import os
import pygame
import json
import random
import options

from utils.color import Color, rgb, random as random_color
from graph.route import get_graph


BLOCK_SIZE = 1700
TASK_SIZE = 10


VEHICLE_COLOR = {
    0: rgb(255, 0, 0),  # WAIT
    1: rgb(195, 0, 0),  # ALLOC
    2: rgb(195, 0, 0),  # MOVE_TO_LOAD
    3: rgb(165, 0, 0),  # LOAD_START
    4: rgb(165, 0, 0),  # LOADING
    5: rgb(165, 0, 0),  # LOAD_END
    6: rgb(105, 0, 0),  # MOVE_TO_UNLOAD
    7: rgb(75, 0, 0),   # UNLOAD_START
    8: rgb(75, 0, 0),   # UNLOADING
    9: rgb(75, 0, 0),   # UNLOAD_END
}


ROAD_COLOR = {
    1: rgb(0, 255, 0),
    2: rgb(255, 212, 0),
    3: rgb(238, 85, 19),
    4: rgb(210, 24, 24),
}

TASK_COLOR = {}


def to_pygame_color(color: Color) -> pygame.color.Color:
    return pygame.color.Color(
        int(255 * color.get_red()),
        int(255 * color.get_green()),
        int(255 * color.get_blue()),
    )


def get_road_color(weight: int) -> tuple[int, int, int]:
    color: Color = ROAD_COLOR[weight] if weight in ROAD_COLOR else rgb(0, 0, 0)
    return to_pygame_color(color)


def draw_road(surface, node, graph):
    for edge in graph.edges():
        weight: int = graph.get_edge_data(edge[0], edge[1])['weight']

        pygame.draw.line(surface, get_road_color(weight),
                         ((node[edge[0]][1] - MIN[1]) * BLOCK_SIZE,
                          500 - (node[edge[0]][0] - MIN[0]) * BLOCK_SIZE),
                         ((node[edge[1]][1] - MIN[1]) * BLOCK_SIZE, 500 - (node[edge[1]][0] - MIN[0]) * BLOCK_SIZE))


def read_log(log_path):
    with open(log_path, 'r') as file:
        logs = json.load(file)

    return logs['logs']


def draw_vehicle(surface, loc):
    surface.blit(taxi_image, ((loc[1] - MIN[1]) * BLOCK_SIZE,
                 500 - (loc[0] - MIN[0]) * BLOCK_SIZE))


def draw_vehicles(surface, vehicles):
    for vehicle in vehicles:
        loc = (vehicle['lat'], vehicle['lng'])

        draw_vehicle(surface, loc)


def draw_load_task(surface, t_idx, loc):
    loc = ((loc[1] - MIN[1]) * BLOCK_SIZE,
           500 - (loc[0] - MIN[0]) * BLOCK_SIZE)
    pygame.draw.circle(surface, to_pygame_color(
        TASK_COLOR[t_idx % 100]), loc, TASK_SIZE / 2)


def draw_unload_task(surface, t_idx, loc):
    loc = ((loc[1] - MIN[1]) * BLOCK_SIZE,
           500 - (loc[0] - MIN[0]) * BLOCK_SIZE)
    pygame.draw.circle(surface, to_pygame_color(
        TASK_COLOR[t_idx % 100]), loc, TASK_SIZE / 2, 3)


def draw_tasks(surface, tasks):
    for task in tasks:
        t_idx = task['id']
        status = task['status']
        if 0 <= status <= 4:
            draw_load_task(
                surface, t_idx, (task['pick_lat'], task['pick_lng']))
            draw_unload_task(
                surface, t_idx, (task['drop_lat'], task['drop_lng']))
        elif 5 <= status <= 8:
            draw_unload_task(
                surface, t_idx, (task['drop_lat'], task['drop_lng']))
        elif status == 9:
            continue
        else:
            print("Error")


def set_task_color():
    random.seed(0)
    for i in range(100):
        TASK_COLOR[i] = random_color()


if __name__ == "__main__":
    DIR = os.path.dirname(os.path.abspath(__file__))
    TAXI_IMAGE_PATH = os.path.join(DIR, 'taxi.jpg')
    opts: dict = options.get_options()
    LOG_PATH = opts["--log-file"] or None
    if LOG_PATH is None:
        print(opts["--help"])
        exit(2)

    taxi_image = pygame.image.load(TAXI_IMAGE_PATH)
    taxi_image = pygame.transform.scale(taxi_image, (10, 10))

    logs = read_log(LOG_PATH)
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
