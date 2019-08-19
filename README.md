# Overview

This is a sample project to show of the capabilities of the pytest
framework.

Source code and a sample etl job is under `src/` and test examples
are under `test/`.

The etl job read a public s3 bucket that contains
New York City taxi data, runs a passenger count summation
on the data, and stores the result on the local filesystem
under a new folder `./data`.

## Installation

In a new virtual environment, run 

```bash
> pip install -r requirements.txt -r requirements-dev.txt
```

## Configuration

The script needs two environment variables that correspond to the report
that needs to be processed.  Taxi reports are a monthly job.
* MONTH
* YEAR

[See the bucket!](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

## Running

From inside the `src` directory, run

```bash
> env MONTH=01 YEAR=2019 python -m taxi_trips
```

## Unit Tests

From the project directory run

```bash
> tox
```

## Integration Tests

From the project directory run

```bash
> tox -e integration
```

## Test Structure

Within the `test` package:
* `test_pytest_basics.py` contains an overview of pytest features
* `conftest.py` contains shared pytest fixtures
* `test_passenger_count.py` contains unit test for the sample job
* `test_passenger_count_integration.py` contains an example integration test for the job

If you're new to pytest, `test_pytest_basics.py` is a good place to start!
