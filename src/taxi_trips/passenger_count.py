import os
import io
import logging
import csv
import requests

logger = logging.getLogger(__name__)

YELLOW_TAXI_ENDPOINT = 'https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_{year}-{month}.csv'
REQUEST_TIMEOUT_SECONDS = 5

FILE_FORMAT = '{year}_{month}_count_passengers.csv'
RESULT_PATH = 'data/'


def start_job(config=os.environ):
    logger.info('Starting count_passengers job')
    taxi_report = pull_file(year=config['YEAR'], month=config['MONTH'])
    number_of_passengers = count_people(taxi_report)
    save_csv_file(year=config['YEAR'], month=config['MONTH'], results=number_of_passengers)
    logger.info('Finished count_passengers job')


def pull_file(year, month):
    url = YELLOW_TAXI_ENDPOINT.format(year=year, month=month)

    logger.info(f'Started pulling file from {url}')
    response = requests.get(url, allow_redirects=True, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    logger.info(f'Finished pulling file from {url} with status code: {response.status_code}')

    return io.StringIO(response.text)


def count_people(taxi_report):
    logger.info('Starting read csv report')
    csv_reader = csv.DictReader(taxi_report)
    passenger_count = 0
    for row in csv_reader:
        try:
            passenger_count += int(row['passenger_count'])
        except KeyError:
            logger.error('Missing passenger_count on line: {}'.format(csv_reader.line_num))
        except ValueError:
            logger.error('Failed to parse passenger_count on line: {}'.format(csv_reader.line_num))
    logger.info('Finished reading csv')

    return passenger_count


def save_csv_file(year, month, results):
    file_key = FILE_FORMAT.format(year=year, month=month)
    filename = '{path}{file_key}'.format(file_key=file_key, path=RESULT_PATH)

    if not os.path.exists(os.path.dirname(RESULT_PATH)):
        os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)

    with open(filename, 'w') as csv_file:
        fieldnames = ['passenger_count']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'passenger_count': results})

    logger.info('Saved passenger count report to {filename}'.format(filename=filename))

    return filename
