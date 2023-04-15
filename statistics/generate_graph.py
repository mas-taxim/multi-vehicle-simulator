import pandas as pd
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import json


def read_log(f_name):
    with open(f'log/{f_name}', 'r') as file:
        logs = json.load(file)
    return pd.DataFrame(logs['task']).transpose(), pd.DataFrame(logs['vehicle']).transpose()


def generate_task_graph(log_df: pd.DataFrame):
    # Data preprocessing
    log_df['last_update_time'] = pd.to_datetime(
        log_df['last_update_time'], unit='ms')
    log_df['create_time'] = pd.to_datetime(log_df['create_time'], unit='ms')
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

    grouping_df.rename(columns={'create_time': 'Time'}, inplace=True)

    # ploting Data
    plt.figure(figsize=(8, 4))
    # plt.rcParams['font.family'] = 'AppleGothic'
    # plt.rcParams['font.family'] = 'NanumGothic'
    # plt.title("시간대 별 배차 후 대기시간 평균", fontsize=25)
    sns.barplot(x='Time', y='wait_vehicle_time', data=grouping_df)
    # sns.lineplot(x = 'create_time', y='wait_alloc_time', data = grouping_df)
    plt.savefig("./img/wait-vehicle-time.png")

    plt.figure(figsize=(8, 4))
    # plt.rcParams['font.family'] = 'AppleGothic'
    # plt.rcParams['font.family'] = 'NanumGothic'
    # plt.title("시간대 별 배차 대기시간 평균")
    sns.barplot(x='Time', y='wait_alloc_time', data=grouping_df)
    plt.savefig("./img/wait-alloc-time.png")

    plt.figure(figsize=(8, 4))
    # plt.rcParams['font.family'] = 'AppleGothic'
    # plt.rcParams['font.family'] = 'NanumGothic'
    # plt.title("시간대 별 배차요청-탑승 대기시간 평균")
    sns.barplot(x='Time', y='wait_total_time', data=grouping_df)
    plt.savefig("./img/wait-total-time.png")

    return


def generate_vehicle_graph(log_df: pd.DataFrame):
    # summary Data
    v_alloc_time_avg = log_df['wait_alloc_time'].mean()
    v_moving_to_load_time = log_df['moving_to_load_time'].mean()

    event_list = []

    for v_event in log_df['empty_event']:
        first_event = True
        for event in v_event:
            if first_event:
                first_event = False
                continue
            event_list.append(event)

    event_df = pd.DataFrame(event_list, columns=['time', 'empty_time'])
    event_df['time'] = pd.to_datetime(event_df['time'], unit='ms')


    # to koran time
    event_df['time'] = pd.DatetimeIndex(event_df['time'] + timedelta(hours=9))

    # grouping Data
    event_df_g = event_df.groupby([pd.Grouper(key='time', freq='1H')])[
        'empty_time'].mean().reset_index().sort_values(['time'])
    event_df_g['Time'] = event_df_g['time'].dt.hour

    # ploting Data
    plt.figure(figsize=(8, 4))
    # plt.rcParams['font.family'] = 'NanumGothic'
    # plt.rcParams['font.family'] = 'AppleGothic'
    # plt.title("시간대 별 택시 공차시간 평균")
    sns.barplot(x='Time', y='empty_time', data=event_df_g)
    plt.savefig("./img/vehicle-empty-time.png")

    return v_alloc_time_avg, v_moving_to_load_time


# task 시간 histogram (배차 대기 시간, 배차 후 대기 시간, 이동 시간)
def generate_task_histogram(f_name, df_task):
    # Data preprocessing
    df_task['total_wait_time'] = df_task['wait_alloc_time'] + df_task['wait_vehicle_time']

    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(8, 12))
    fig.tight_layout()
    plt.suptitle(f'Task Histogram {f_name}')
    plt.subplots_adjust(hspace=0.3, top=0.95, bottom=0.08, left=0.08)

    plt.subplot(411)
    sns.histplot(data=df_task['wait_alloc_time'])
    plt.axvline(x=df_task['wait_alloc_time'].mean(), color='red')
    plt.text(df_task['wait_alloc_time'].mean() + 1, 1, round(df_task['wait_alloc_time'].mean(), 2), color='red')

    plt.subplot(412)
    sns.histplot(data=df_task['wait_vehicle_time'])
    plt.axvline(x=df_task['wait_vehicle_time'].mean(), color='red')
    plt.text(df_task['wait_vehicle_time'].mean() + 1, 1, round(df_task['wait_vehicle_time'].mean(), 2), color='red')

    plt.subplot(413)
    sns.histplot(data=df_task['total_wait_time'])
    plt.axvline(x=df_task['total_wait_time'].mean(), color='red')
    plt.text(df_task['total_wait_time'].mean() + 1, 1, round(df_task['total_wait_time'].mean(), 2), color='red')

    plt.subplot(414)
    sns.histplot(data=df_task['moving_time'])
    plt.axvline(x=df_task['moving_time'].mean(), color='red')
    plt.text(df_task['moving_time'].mean() + 1, 1, round(df_task['moving_time'].mean(), 2), color='red')
    # plt.show()

    plt.savefig(f'images/{f_name.split(".")[0]}_task.png')

    return


# task 시간 histogram (배차 대기 시간, 배차 후 대기 시간, 이동 시간)
def generate_vehicle_histogram(f_name, df_vehicle):
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(8, 8))
    fig.tight_layout()
    plt.suptitle(f'Vehicle Histogram {f_name}')
    plt.subplots_adjust(hspace=0.3, top=0.95, bottom=0.08, left=0.08)
    plt.subplot(311)

    plt.subplot(311)
    sns.histplot(data=df_vehicle['wait_alloc_time'])
    plt.axvline(x=df_vehicle['wait_alloc_time'].mean(), color='red')

    plt.subplot(312)
    sns.histplot(data=df_vehicle['moving_to_load_time'])
    plt.axvline(x=df_vehicle['moving_to_load_time'].mean(), color='red')

    plt.subplot(313)
    sns.histplot(data=df_vehicle['moving_time'])
    plt.axvline(x=df_vehicle['moving_time'].mean(), color='red')
    # plt.show()

    plt.savefig(f'images/{f_name.split(".")[0]}_vehicle.png')

    return


def generate_image(logData: dict):
    print(os.getcwd())
    generate_task_graph(pd.DataFrame(logData['task']).T)
    generate_vehicle_graph(pd.DataFrame(logData['vehicle']).T)

    return


def generate_histogram(f_name):
    df_task, df_vehicle = read_log(f_name)
    generate_task_histogram(f_name, df_task)
    # generate_vehicle_histogram(f_name, df_vehicle)
