import os
import logging
import csv
import requests

from taxi_trips import job_runner

logger = logging.getLogger(__name__)

YELLOW_TAXI_ENDPOINT = 'https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_{year}-{month}.csv'

JOB_NAME = 'count_passengers'
FILE_FORMAT = '{year}_{month}_{name}{checkpoint_handle}.csv'
CHECKPOINT_HANDLE_FORMAT = '_stage={stage_counter}-{job_name}'
RESULT_PATH = 'data/results/'
CHECKPOINT_PATH = 'data/checkpoint/'


def start_job(config=os.environ):
    stages = [
        job_runner.JobStage(job=pull_file, params={
            'year': config['YEAR'],
            'month': config['MONTH']
        }),
        job_runner.JobStage(job=count_people)
    ]
    logger.info('Starting passenger_count job')
    job_runner.run_linear_stages(stages, config)
    logger.info('Finished passenger_count job')


def pull_file(year, month):
    url = YELLOW_TAXI_ENDPOINT.format(year, month)

    logger.info(f'Started pulling file from {url}')
    response = requests.get(url, allow_redirects=True)
    logger.info(f'Finished pulling file from {url} with status code: {response.status_code}')

    return response.content


def count_people(previous_checkpoint):
    logger.info('Starting count passenger stage. Reading checkpoint: {}'.format(previous_checkpoint))
    with open(previous_checkpoint) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        passenger_count = 0
        for row in csv_reader:
            try:
                passenger_count += int(row['passenger_count'])
            except ValueError:
                logger.error('Failed to parse passenger_count on line: {}'.format(csv_reader.line_num))
    logger.info('Finished count passenger stage')

    return str(passenger_count)
