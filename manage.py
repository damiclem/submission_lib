import logging

import drmaa as dr

from .session import Session
from .slurm.job import Job

logger = logging.getLogger(__name__)

session = Session()
session.start()


def start_job(working_dir, script_args, script_dir="/home/alessio/projects/submission_ws/scripts",
              out_dir="/home/alessio/projects/submission_ws/outputs", is_array=False, begin_index=1, end_index=1,
              step_index=1, **kwargs):
    job: Job = Job(working_dir=working_dir, script_dir=script_dir, output_base_pth=out_dir, args=script_args, **kwargs)

    name = job.get_name()

    if is_array:
        j_ids = session.runBulkJobs(job.get_instance(), beginIndex=begin_index, endIndex=end_index, step=step_index)
        j_id = j_ids[0].split('_')[0]
        logger.debug("Array job %s started with id %s", name, j_id)
    else:
        j_id = session.runJob(job.get_instance())
        logger.debug("Job %s started with id %s", name, j_id)

    # logger.info('Cleaning up')
    session.deleteJobTemplate(job)
    return j_id, name


def get_job_status(j_id: str):
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

    status = session.jobStatus(j_id)
    logger.debug("Status for job %s: %s", j_id, decodestatus[status])
    return decodestatus[status]


def terminate_job(j_id):
    session.terminate_job(str(j_id))


if __name__ == '__main__':
    pass
