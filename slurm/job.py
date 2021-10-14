from typing import List

from job import AbstractJob, ConcurrentArgumentError, EmailType
from params import ScriptParam


class EmailType(EmailType):
    NONE = "NONE"
    BEGIN = "BEGIN"
    END = "END"
    FAIL = "FAIL"
    REQUEUE = "REQUEUE"
    ALL = "ALL"


class Job(AbstractJob):
    def __init__(self, name: str, command: str, working_dir: str, output_file: str, error_file: str, script_dir: str,
                 output_base_pth: str, queue: str = "local", nodes: int = 1, n_tasks_per_node: int = 1,
                 cpus_per_task: int = 1, n_tasks: int = 1, mem_per_node: str = None, mem_per_cpu: str = None,
                 clock_time_limit: str = None, email_address: str = None, email_type: EmailType = EmailType.ALL,
                 account: str = None, args: List[ScriptParam] = None):
        super().__init__(name, command, working_dir, output_file, error_file, script_dir, output_base_pth, queue, nodes,
                         n_tasks_per_node, cpus_per_task, n_tasks, mem_per_node, mem_per_cpu, clock_time_limit,
                         email_address, email_type, account, args)
        self._is_mem_per_cpu = False
        self._is_mem_per_node = False


    def use_queue(self, q_name: str):
        if len(q_name) == 0:
            raise ValueError
        self._queue = q_name
        self._job.nativeSpecification += " --partition={}".format(q_name)

    def set_node_count(self, node_count: int):
        self._job.nativeSpecification += " --nodes={}".format(node_count)

    def set_ntasks_per_node(self, n_tasks: int):
        self._job.nativeSpecification += " --ntasks-per-node={}".format(n_tasks)

    def set_cpus_per_task(self, ncpus: int):
        self._job.nativeSpecification += " --cpus-per-task={}".format(ncpus)

    def set_ntasks(self, n_tasks: int):
        self._job.nativeSpecification += " --ntasks={}".format(n_tasks)

    def set_mem_per_node(self, mem: str):
        if self._is_mem_per_cpu:
            raise ConcurrentArgumentError("mem_per_cpu")
        self._job.nativeSpecification += " --mem={}".format(mem)
        self._is_mem_per_node = True

    def set_mem_per_cpu(self, mem: str):
        if self._is_mem_per_node:
            raise ConcurrentArgumentError("mem_per_node")
        self._job.nativeSpecification += " --mem-per-cpu={}".format(mem)
        self._is_mem_per_cpu = True

    def set_email_type(self, notification_type: EmailType):
        self._job.nativeSpecification += " --mail-type={}".format(notification_type)

    def set_account(self, a: str):
        self._job.nativeSpecification += " --account={}".format(a)
