import logging

import drmaa as dr

from .session import Session
from .slurm.job import Job

logging.basicConfig(level=logging.DEBUG,
                    filename='logger.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def start_job(working_dir, script_args, script_dir="/home/alessio/projects/submission_ws/scripts",
              out_pth="/home/alessio/projects/submission_ws/outputs", **kwargs):
    session = Session()
    session.start()
    job: Job = Job(working_dir=working_dir, script_dir=script_dir, output_base_pth=out_pth, **kwargs)

    job.args = script_args
    name = job.get_name()
    logger.info(name)
    j_id = session.runJob(job)
    logger.info('Your job has been submitted with ID %s', j_id)

    logger.info('Cleaning up')
    session.deleteJobTemplate(job)
    session.stop()
    return j_id, name


def check_job_status(j_id):
    session = Session()
    session.start()
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
    session.stop()


if __name__ == '__main__':
    pass
