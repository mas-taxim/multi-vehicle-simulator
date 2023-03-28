import pandas as pd
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns


def generate_task_graph(log_df: pd.DataFrame):

    # Data preprocessing
    log_df['last_update_time'] = pd.to_datetime(
        log_df['last_update_time'], unit='ms')
    log_df['create_time'] = pd.to_datetime(log_df['create_time'], unit='ms')
    log_df['wait_alloc_time'] /= 60000
    log_df['wait_vehicle_time'] /= 60000
    log_df['wait_total_time'] = log_df['wait_alloc_time'] + \
        log_df['wait_vehicle_time']

    # to koran time
    log_df['last_update_time'] = pd.DatetimeIndex(
        log_df['last_update_time'] + timedelta(hours=9))
    log_df['create_time'] = pd.DatetimeIndex(
        log_df['create_time'] + timedelta(hours=9))

    # grouping Data
    grouping_df = log_df.groupby([pd.Grouper(key='create_time', freq='1H')])[
        'wait_vehicle_time', 'wait_alloc_time', 'wait_total_time'].mean().reset_index().sort_values(['create_time'])
    grouping_df['create_time'] = grouping_df['create_time'].dt.hour

    # ploting Data
    plt.figure(figsize=(8, 4))
    sns.barplot(x='create_time', y='wait_vehicle_time', data=grouping_df)
    #sns.lineplot(x = 'create_time', y='wait_alloc_time', data = grouping_df)
    plt.savefig("./img/wait-vehicle-time.png")

    plt.figure(figsize=(8, 4))
    sns.barplot(x='create_time', y='wait_alloc_time', data=grouping_df)
    plt.savefig("./img/wait-alloc-time.png")

    plt.figure(figsize=(8, 4))
    sns.barplot(x='create_time', y='wait_total_time', data=grouping_df)
    plt.savefig("./img/wait-total-time.png")

    return


def generate_vehicle_graph(log_df: pd.DataFrame):

    # Data preprocessing
    log_df['wait_alloc_time'] /= 60000
    log_df['moving_to_load_time'] /= 60000

    # summary Data
    v_alloc_time_avg = log_df['wait_alloc_time'].mean()
    v_moving_to_load_time = log_df['moving_to_load_time'].mean()

    event_list = []

    for v_event in log_df['empty_event']:
        for event in v_event:
            event_list.append(event)

    event_df = pd.DataFrame(event_list, columns=['time', 'empty_time'])
    event_df['time'] = pd.to_datetime(event_df['time'], unit='ms')
    event_df['empty_time'] /= 60000

    # to koran time
    event_df['time'] = pd.DatetimeIndex(event_df['time'] + timedelta(hours=9))

    # grouping Data
    event_df_g = event_df.groupby([pd.Grouper(key='time', freq='1H')])[
        'empty_time'].mean().reset_index().sort_values(['time'])
    event_df_g['time'] = event_df_g['time'].dt.hour

    # ploting Data
    plt.figure(figsize=(8, 4))
    sns.barplot(x='time', y='empty_time', data=event_df_g)
    plt.savefig("./img/vehicle-empty-time.png")

    return v_alloc_time_avg, v_moving_to_load_time


def generate_image(logData: dict):
    print(os.getcwd())
    generate_task_graph(pd.DataFrame(logData['task']).T)
    generate_vehicle_graph(pd.DataFrame(logData['vehicle']).T)

    return
