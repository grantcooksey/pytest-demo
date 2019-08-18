import logging
import os

logger = logging.getLogger(__name__)

FILE_FORMAT = '{year}_{month}_{name}{checkpoint_handle}.csv'
CHECKPOINT_HANDLE_FORMAT = '_stage={stage_counter}-{job_name}'
RESULT_PATH = 'data/results/'
CHECKPOINT_PATH = 'data/checkpoint/'


def run_linear_stages(job_name, stages, config):
    previous_checkpoint = None
    for stage_counter, stage in enumerate(stages[:-1]):
        if previous_checkpoint is None:
            logger.info('Starting stage number: {stage_counter}. Running {stage_name}'.format(
                stage_counter=stage_counter,
                stage_name=stage.job.__name__
            ))
            result = stage.job(**stage.params)
        else:
            result = stage.job(previous_checkpoint, **stage.params)
        previous_checkpoint = checkpoint(
            job_name,
            config['YEAR'],
            config['MONTH'],
            content=result,
            stage_counter=stage_counter
        )

    # TODO: Add logging
    final_stage = stages[-1]
    result = final_stage.job(previous_checkpoint, **final_stage.params)
    checkpoint(job_name, config['YEAR'], config['MONTH'], content=result)


def checkpoint(job_name, year, month, content, stage_name=None, stage_counter=None):
    if stage_counter is None:
        path = CHECKPOINT_PATH
        file_key = FILE_FORMAT.format(year=year, month=month, name=job_name, checkpoint_handle='')
    else:
        path = RESULT_PATH
        file_key = FILE_FORMAT.format(
            year=year,
            month=month,
            name=job_name,
            checkpoint_handle=CHECKPOINT_HANDLE_FORMAT.format(stage_counter=stage_counter, stage_name=stage_name)
        )
    filename = '{path}{file_key}'.format(file_key=file_key, path=path)

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(filename, 'wb') as f:
        f.write(content)

    return filename


class JobStage:
    def __init__(self, job, params=None):
        self.job = job
        if params is None:
            self.params = {}
        else:
            self.params = params
