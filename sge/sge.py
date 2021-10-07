from job import AbstractJob, EmailType


class Job(AbstractJob):
    def use_queue(self, q_name: str):
        if len(q_name) == 0:
            raise ValueError
        self._queue = q_name
        self._job.nativeSpecification += " -q {}".format(q_name)

    def set_node_count(self, node_count: int):
        pass

    def set_ntasks_per_node(self, n_tasks: int):
        pass
        # self._job.nativeSpecification += " --ntasks-per-node={}".format(n_tasks)

    def set_cpus_per_task(self, ncpus: int):
        self._job.nativeSpecification += " -pe multithread {}".format(ncpus)

    def set_ntasks(self, n_tasks: int):
        self._job.nativeSpecification += " -pe multithread {}".format(n_tasks)

    def set_mem_per_node(self, mem: str):
        self._job.nativeSpecification += " -l mem_free={}".format(mem)

    def set_mem_per_cpu(self, mem: str):
        self._job.nativeSpecification += " -l mem_free={}".format(mem)

    def set_email_type(self, notification_type: EmailType):
        self._job.nativeSpecification += " --mail-type={}".format(notification_type)

    def set_account(self, a: str):
        self._job.nativeSpecification += " -A {}".format(a)
