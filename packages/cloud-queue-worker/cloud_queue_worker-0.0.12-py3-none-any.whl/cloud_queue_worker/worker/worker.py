import signal
from time import sleep
from multiprocessing import Process, Event, Queue, Value
from typing import Dict, List, Any, Optional, Tuple, overload
from queue import Empty
from abc import ABC, abstractmethod
import os
import importlib
from uuid import uuid4
from types import FunctionType
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from ..utils import get_client
from ..logging import logger
from .errors import QueueArgumentError, WorkerResultUnknown
from .enums import WorkerResult


class Worker(Process, ABC):
    def __init__(self, internal_queue: Queue, cloud_provider_config: Dict[str, str], *args, **kwargs) -> None:
        """
        Main abstract class used to create read/write workers.
        :param internal_queue: Internal queue used to pass data between workers.
        :param cloud_provider_config: cloud provider config dict used to get appropriate client.
        """
        super().__init__(*args, **kwargs)
        self.internal_queue = internal_queue
        self.cloud_provider_config = cloud_provider_config
        self.exit = Event()

    @abstractmethod
    def run(self):
        pass


class ReadWorker(Worker):
    def __init__(
            self, internal_queue: Queue, cloud_provider_config: Dict[str, str], queue_url: str,
            internal_queue_size: Value
    ) -> None:
        """
        Read worker class. His role is the fetch messages from cloud provider queues
        and send them to internal queue to be processed by executor's workers.
        :param internal_queue: Internal queue used to pass data between workers.
        :param cloud_provider_config: cloud provider config dict used to get appropriate client.
        :param queue_url: Queue's url related to the worker
        :param internal_queue_size: A Value param containing a integer to know the size of the internal queue. We cannot use qsize, Empty or full as it's specified in the multiprocessing documentation as non reliable (https://docs.python.org/3.8/library/multiprocessing.html#multiprocessing.Queue.qsize)
        """
        super().__init__(internal_queue, cloud_provider_config)
        self._queue_url = queue_url
        self.name = queue_url
        self.internal_queue_size = internal_queue_size

    def run(self) -> None:
        """
        Start ReadWorker
        """
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        client = get_client(self.cloud_provider_config)
        logger.debug("The read worker with pid %d", os.getpid())
        while not self.exit.is_set():
            if self.internal_queue_size.value < 50:
                messages = self._fetch_messages(client)
                if messages:
                    self._send_messages_to_executor(messages)
            else:
                sleep(1)
        logger.debug("a signal has been received to close the read worker with pid %d", os.getpid())

    def _fetch_messages(self, client) -> List[Any]:
        """
        Fetch messages from cloud provider queue.
        :param client: Cloud provider client used to fetch messages
        """
        logger.debug("fetch messages from read worker")
        return client.receive_message(QueueUrl=self._queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=20).get(
            "Messages", []
        )

    def _send_messages_to_executor(self, messages: List[Any]) -> None:
        """
        Wrap messages with internal required data and send them to FIFO multiprocessing queue.
        :param messages: A list of messages.
        """
        logger.debug("send messages to executor")
        for message in messages:
            internal_message = {"message": message, "queue_url": self._queue_url}
            self.internal_queue.put(internal_message)
            with self.internal_queue_size.get_lock():
                self.internal_queue_size.value += 1


class ExecutorWorker(Worker):
    def __init__(
            self, queue_mapping: Dict[str, str], internal_queue: Queue, cloud_provider_config: Dict[str, str],
            internal_queue_size: Value
    ) -> None:
        """
        :param queue_mapping: Dict used to make the relation between the cloud provider queue
        and the worker used to process data.
        :param internal_queue: Internal queue used to pass data between workers.
        :param cloud_provider_config: cloud provider config dict used to get appropriate client.
        :param internal_queue_size: A Value param containing a integer to know the size of the internal queue. We cannot use qsize, Empty or full as it's specified in the multiprocessing documentation as non reliable (https://docs.python.org/3.8/library/multiprocessing.html#multiprocessing.Queue.qsize)
        """
        super().__init__(internal_queue, cloud_provider_config)
        self.queue_mapping = queue_mapping
        self.function_mapping = self._initialize_function_mapping()
        self.internal_queue_size = internal_queue_size

    def run(self) -> None:
        """
        Start ExecutorWorker
        """
        logger.debug("The executor worker with pid %d has been started", os.getpid())
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        client = get_client(self.cloud_provider_config)
        while not self.exit.is_set() or not self.internal_queue.empty():
            message = self._fetch_message()
            if message:
                res = self._handle_message(message)
                if not res or res == WorkerResult.ACK:
                    self._acknowledge(message, client)
                elif res[0] == WorkerResult.UNACK:
                    visibility_timeout = res[1].get("visibility_timeout", 30)
                    self._resend_message(message, client, visibility_timeout)
                else:
                    raise WorkerResultUnknown(f"Wrong return type : {type(res[0])}")

        logger.debug("a signal has been received to close the executor worker with pid %d", os.getpid())

    def _fetch_message(self) -> Optional[Dict[str, Any]]:
        """
        Fetch message from internal queue.
        :returns: Dict if there are data to process else None.
        """
        try:
            message = self.internal_queue.get(timeout=0.5)
            with self.internal_queue_size.get_lock():
                if self.internal_queue_size.value > 0:
                    self.internal_queue_size.value -= 1
            return message
        except Empty:
            return None

    def _resend_message(self, message: Dict[str, Any], client, visibility_timeout: int):
        """
        Change the visibility timeout of the message
        :param message: internal queue's message.
        :param client: Cloud provider's client.
        :param visibility_timeout: ew visibility timeout
        :return:
        """
        logger.debug("resend message")
        client.change_message_visibility(
            QueueUrl=message["queue_url"],
            ReceiptHandle=message["message"]["ReceiptHandle"],
            VisibilityTimeout=visibility_timeout
        )

    @overload
    def _handle_message(self, message: Dict[str, Any]) -> Tuple[Literal[WorkerResult.UNACK], Dict[str, Any]]:
        ...

    @overload
    def _handle_message(self, message: Dict[str, Any]) -> Literal[WorkerResult.ACK]:
        ...

    @overload
    def _handle_message(self, message: Dict[str, Any]) -> None:
        ...

    def _handle_message(self, message):
        """
        Execute the function related to the message.
        :param message: internal queue's message.
        :type message: dict
        """
        logger.debug("handle message from executor worker")
        function, kwargs = self.function_mapping[message["queue_url"]]
        return function(message["message"], **kwargs)

    def _acknowledge(self, message: Dict[str, Any], client):
        """
        Acknowledge the message at the end of the function's execution.
        :param message: internal queue's message.
        :param client: Cloud provider's client.
        """
        logger.debug("acknowledge message")
        client.delete_message(QueueUrl=message["queue_url"], ReceiptHandle=message["message"]["ReceiptHandle"])

    def _initialize_function_mapping(self):
        function_mapping = {}
        for key, value in self.queue_mapping.items():
            if isinstance(value, str):
                handler_path = value
                handler_kwargs = {}
            elif isinstance(value, tuple) and len(value) == 2:
                handler_path = value[0]
                handler_kwargs = value[1]
            else:
                raise QueueArgumentError(f"Wrong argument type : {value}")
            function_name = handler_path.split(".")[-1]
            function_path = ".".join(handler_path.split(".")[:-1])

            function_module = importlib.import_module(function_path)
            obj = getattr(function_module, function_name)
            if isinstance(obj, FunctionType):
                function_mapping[key] = (obj, handler_kwargs)
            elif issubclass(obj, AbsCustomWorker):
                instance = obj()
                function_mapping[key] = (instance.run, handler_kwargs)
            else:
                raise QueueArgumentError(f"Wrong object type : {type(obj)}")

        return function_mapping


class AbsCustomWorker(ABC):
    def __init__(self):
        self.worker_id = str(uuid4())

    @abstractmethod
    def run(self, msg, **kwargs):
        pass
