import pygame
import json

BLOCK_SIZE = 20
TASK_SIZE = 12

VEHICLE_COLOR = {
    0: (255, 0, 0),
    1: (225, 0, 0),
    2: (195, 0, 0),
    3: (165, 0, 0),
    4: (135, 0, 0),
    5: (105, 0, 0),
}

TASK_COLOR = {
    0: (0, 255, 0),
    1: (0, 225, 0),
    2: (0, 195, 0),
    3: (0, 165, 0),
    4: (0, 135, 0),
    5: (0, 105, 0),
}


def read_log(log_path):
    logs = []

    for line in open(log_path, 'r'):
        logs.append(json.loads(line))

    return logs


def draw_vehicle(surface, status, loc):
    pygame.draw.rect(surface, VEHICLE_COLOR[status], (loc[0] * BLOCK_SIZE, loc[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def draw_vehicles(surface, vehicles):
    for vehicle in vehicles:
        status = vehicle['status']
        loc = (vehicle['loc.x'], vehicle['loc.y'])

        draw_vehicle(surface, status, loc)


def draw_task(surface, status, loc):
    loc = (loc[0] * BLOCK_SIZE + BLOCK_SIZE / 2, loc[1] * BLOCK_SIZE + BLOCK_SIZE / 2)
    pygame.draw.circle(surface, TASK_COLOR[status], loc, TASK_SIZE / 2)


def draw_tasks(surface, tasks):
    for task in tasks:
        status = task['status']
        if status == 5:
            continue
        loc = (task['loc.x'], task['loc.y'])

        draw_task(surface, status, loc)


logs = read_log("../log/20230112_150355.log")

pygame.init()
screen = pygame.display.set_mode((20 * BLOCK_SIZE, 20 * BLOCK_SIZE))

log_idx = 0

while True:
    log = logs[log_idx]
    n_time = log['n_time']
    vehicles = log['vehicle']['vehicle_log']
    tasks = log['task']['task_log']

    screen.fill((0, 0, 0))

    draw_vehicles(screen, vehicles)
    draw_tasks(screen, tasks)

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
