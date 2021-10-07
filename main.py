import json
import logging
from typing import Dict

import drmaa as dr

from params import ScriptParam
from slurm.job import Job
from utils import Session, make_token

session = Session()

jobs: Dict[str, str] = dict()
logger = logging.getLogger(__name__)


def start_job(j_params, params, script_dir, out_pth):
    job: Job = Job(script_dir=script_dir, output_base_pth=out_pth, **j_params)

    job.args = params

    j_id = session.runJob(job)
    # jobs.setdefault(job._job.jobName, j_id)
    logger.info('Your job has been submitted with ID %s', j_id)

    logger.info('Cleaning up')
    session.deleteJobTemplate(job)
    return j_id


def check_job_status(j_id):
    # Who needs a case statement when you have dictionaries?
    decodestatus = {dr.JobState.UNDETERMINED       : 'process status cannot be determined',
                    dr.JobState.QUEUED_ACTIVE      : 'job is queued and active',
                    dr.JobState.SYSTEM_ON_HOLD     : 'job is queued and in system hold',
                    dr.JobState.USER_ON_HOLD       : 'job is queued and in user hold',
                    dr.JobState.USER_SYSTEM_ON_HOLD: 'job is queued and in user and system hold',
                    dr.JobState.RUNNING            : 'job is running',
                    dr.JobState.SYSTEM_SUSPENDED   : 'job is system suspended',
                    dr.JobState.USER_SUSPENDED     : 'job is user suspended',
                    dr.JobState.DONE               : 'job finished normally',
                    dr.JobState.FAILED             : 'job finished, but failed'}

    logger.info("Status for job %s: %s", j_id, decodestatus[session.jobStatus(j_id)])


if __name__ == '__main__':
    session.start()
    with open("job_definition.json", 'r') as f:
        data = json.load(f)

    job_template = data["templates"][0]
    job_template["job"]["working_dir"] = make_token()
    start_job(job_template["job"], [ScriptParam(k, **v) for k, v in job_template["params"].items()],
              data["scripts_dir"], data["output_base_path"])
    session.stop()
