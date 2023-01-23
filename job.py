import logging
import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import List

import drmaa as dr

logger = logging.getLogger(__name__)


class EmailType(Enum):
    NONE = "NONE"
    BEGIN = "BEGIN"
    END = "END"
    FAIL = "FAIL"
    REQUEUE = "REQUEUE"
    ALL = "ALL"


class ConcurrentArgumentError(Exception):
    def __init__(self, argument=""):
        self.message = "The concurrent argument {} was already defined".format(argument)
        super().__init__(self.message)


class AbstractJob(ABC):
    def __init__(self, task_name: str, command: str, working_dir: str, stdout_file: str, stderr_file: str,
                 script_dir: str, output_base_pth: str, queue: str = "local", nodes: int = 1, n_tasks_per_node: int = 1,
                 cpus_per_task: int = 1, n_tasks: int = 1, mem_per_node: str = None, mem_per_cpu: str = None,
                 clock_time_limit: str = None, email_address: str = None, email_type: EmailType = EmailType.ALL,
                 account: str = None, dependencies: List[int] = None, dependency_type: str = None, args: List = None, **kwargs):
        """
        Creates a new Job with the option of specifying some parameters for the scheduler

        :param task_name: The name of the job, different from the job id
        :param queue: The queue where to run the job
        :param command: The path to a sh script or directly a command
        """

        self.output_base_pth = output_base_pth
        self.script_dir = script_dir

        self._job = dr.JobTemplate()
        self._is_deleted = False

        self.tok = ""
        self.set_working_dir(working_dir)
        self.set_name(task_name)
        self.set_command(command)
        self.set_output_path(stdout_file)
        self.set_error_path(stderr_file)
        self._queue = queue
        self.use_queue(self._queue)
        self.set_node_count(nodes)
        self.set_ntasks_per_node(n_tasks_per_node)
        self.set_cpus_per_task(cpus_per_task)
        self.set_ntasks(n_tasks)
        if mem_per_cpu is not None:
            self.set_mem_per_cpu(mem_per_cpu)
        if mem_per_node is not None:
            self.set_mem_per_node(mem_per_node)
        if clock_time_limit is not None:
            self.set_clock_time_limit(clock_time_limit)
        if email_address is not None:
            self.set_email_address(email_address)
        if email_type is not None:
            self.set_email_type(email_type)
        if account is not None:
            self.set_account(account)
        if dependencies is not None:
            self.set_dependencies(dependencies, dependency_type)
        if args is None:
            args = []
        self.args = args

    def get_instance(self) -> dr.JobTemplate:
        return self._job

    def delete(self):
        self._is_deleted = True
        self._job.delete()

    def is_deleted(self):
        return self._is_deleted

    @property
    def args(self):
        return self._job.args

    @args.setter
    def args(self, args: List):
        logger.debug("Setting args to {}".format(args))
        self._job.args = args

    def set_working_dir(self, wd: str):
        """
        :param wd: The path to the working directory of the job
        """
        wd = str(wd)
        self.tok = wd
        os.makedirs(os.path.join(self.output_base_pth, wd), exist_ok=True)
        self._job.workingDirectory = os.path.join(self.output_base_pth, wd)
        logger.debug("Setting working directory to %s", self._job.workingDirectory)

    def set_output_path(self, pth: str):
        self._job.outputPath = ':' + pth

    def set_error_path(self, pth: str):
        self._job.errorPath = ':' + pth

    def set_name(self, task_name: str):
        self._job.jobName = task_name + "-{}".format(self.tok)

    def set_command(self, path: str):
        """
        Set the command to be executed by the cluster

        :param path: Path to the command script
        """
        self._job.remoteCommand = os.path.join(self.script_dir, path)
        logger.debug("Setting script path to %s", self._job.remoteCommand)

    def pass_arguments_to_command(self, args: List) -> None:
        """
        Pass a list of arguments to the command specified with `set_command`

        :param args: A list of arguments to pass to the command
        """
        self._job.args.extend(args)

    def empty_arguments_of_command(self):
        self._job.args = []

    def join_files(self, join: bool) -> None:
        """
        Join the stdout and stderr files in a single output file, specified with `set_output_path`

        :param join: whether to join or not the files
        """
        self._job.joinFiles = join

    def get_name(self):
        return self._job.jobName

    @abstractmethod
    def use_queue(self, q_name: str):
        raise NotImplementedError

    @abstractmethod
    def set_node_count(self, node_count: int):
        """
        :param node_count: Node count required for the job
        """
        raise NotImplementedError

    @abstractmethod
    def set_ntasks_per_node(self, n_tasks: int):
        """
        :param n_tasks: Number of tasks per node (max)
        """
        raise NotImplementedError

    @abstractmethod
    def set_cpus_per_task(self, ncpus: int):
        """
        Multithreading parameter. Request that ncpus be allocated per process.

        :param ncpus: Number of cores per task (threads)
        """
        raise NotImplementedError

    @abstractmethod
    def set_ntasks(self, n_tasks: int):
        """
        :param n_tasks: Number of tasks (processes)
        """
        raise NotImplementedError

    @abstractmethod
    def set_mem_per_cpu(self, mem: str):
        """
        You must ensure that you are not requesting more than the available memory to run jobs on the nodes
        in a given partition, otherwise your job submission will be rejected. You cannot use this in combination
        with `set_mem_per_node`

        :param mem: Amount of memory per core
        """
        raise NotImplementedError

    @abstractmethod
    def set_mem_per_node(self, mem: str):
        """
        You must ensure that you are not requesting more than the available memory to run jobs on the nodes
        in a given partition, otherwise your job submission will be rejected. You cannot use this in combination
        with `set_mem_per_cpu`

        :param mem: Amount of memory per node
        """
        raise NotImplementedError

    def set_clock_time_limit(self, time: str):
        """
        :param time: Wall clock time limit HH:MM
        """
        self._job.hardWallclockTimeLimit = time

    def set_email_address(self, address: str):
        # self._job.blockEmail = True
        self._job.email = [address]

    @abstractmethod
    def set_email_type(self, notification_type: EmailType):
        """
        :param notification_type: Email notification: BEGIN,END,FAIL,ALL
        """
        raise NotImplementedError

    @abstractmethod
    def set_account(self, a: str):
        raise NotImplementedError

    @abstractmethod
    def set_dependencies(self, dependency, dependency_type):
        raise NotImplementedError
