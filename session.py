import logging

import drmaa as dr

logger = logging.getLogger(__name__)


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Session(dr.Session):
    def __init__(self, contactString=None):
        super().__init__(contactString)
        self.is_running = False

    def start(self):
        if not self.is_running:
            super().initialize()
            self.is_running = True
            logger.debug("Session opened")
        else:
            logger.warning("Session already opened")

    def stop(self):
        if self.is_running:
            super().exit()
            self.is_running = False
            logger.debug("Session closed")
        else:
            logger.warning("Session was not open")

    def terminate_job(self, j_id):
        super().control(j_id, dr.JobControlAction.TERMINATE)

    def hold_job(self, j_id):
        super().control(j_id, dr.JobControlAction.HOLD)

    def resume_job(self, j_id):
        super().control(j_id, dr.JobControlAction.RESUME)

    def suspend_job(self, j_id):
        super().control(j_id, dr.JobControlAction.SUSPEND)

    def release_job(self, j_id):
        super().control(j_id, dr.JobControlAction.RELEASE)

    def is_job_undetermined(self, j_id):
        return self.jobStatus(j_id) == dr.JobState.UNDETERMINED

    def is_job_queued_active(self, j_id):
        return self.jobStatus(j_id) == dr.JobState.QUEUED_ACTIVE

    def is_job_user_hold(self, j_id):
        return self.jobStatus(j_id) == dr.JobState.USER_ON_HOLD

    def is_job_system_hold(self, j_id):
        return self.jobStatus(j_id) == dr.JobState.SYSTEM_ON_HOLD

    def is_job_user_and_system_hold(self, j_id):
        return self.jobStatus(j_id) == dr.JobState.USER_SYSTEM_ON_HOLD

    def is_job_running(self, j_id):
        return self.jobStatus(j_id) == dr.JobState.RUNNING

    def is_job_system_suspended(self, j_id):
        return self.jobStatus(j_id) == dr.JobState.SYSTEM_SUSPENDED

    def is_job_user_suspended(self, j_id):
        return self.jobStatus(j_id) == dr.JobState.USER_SUSPENDED

    def is_job_done(self, j_id):
        return self.jobStatus(j_id) == dr.JobState.DONE

    def is_job_failed(self, j_id):
        return self.jobStatus(j_id) == dr.JobState.FAILED
