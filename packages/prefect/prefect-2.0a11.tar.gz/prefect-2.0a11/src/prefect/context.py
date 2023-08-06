"""
Async and thread safe models for passing runtime context data.

These contexts should never be directly mutated by the user.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from logging import Logger
from typing import Dict, List, Optional, Set, Type, TypeVar, Union
from uuid import UUID

import pendulum
from anyio.abc import BlockingPortal, CancelScope
from pendulum.datetime import DateTime
from pydantic import BaseModel, Field

from prefect.client import OrionClient
from prefect.exceptions import MissingContextError
from prefect.flows import Flow
from prefect.futures import PrefectFuture
from prefect.orion.schemas.core import FlowRun, TaskRun
from prefect.orion.schemas.states import State
from prefect.task_runners import BaseTaskRunner
from prefect.tasks import Task

T = TypeVar("T")


class ContextModel(BaseModel):
    """
    A base model for context data that forbids mutation and extra data while providing
    a context manager
    """

    # The context variable for storing data must be defined by the child class
    __var__: ContextVar

    class Config:
        allow_mutation = False
        arbitrary_types_allowed = True
        extra = "forbid"

    def __enter__(self):
        # We've frozen the rest of the data on the class but we'd like to still store
        # this token for resetting on context exit
        object.__setattr__(self, "__token", self.__var__.set(self))
        return self

    def __exit__(self, *_):
        self.__var__.reset(getattr(self, "__token"))

    @classmethod
    def get(cls: Type[T]) -> Optional[T]:
        return cls.__var__.get(None)


class RunContext(ContextModel):
    """
    The base context for a flow or task run. Data in this context will always be
    available when `get_run_context` is called.

    Attributes:
        start_time: The time the run context was entered
        client: The Orion client instance being used for API communication
    """

    start_time: DateTime = Field(default_factory=lambda: pendulum.now("UTC"))
    client: OrionClient


class FlowRunContext(RunContext):
    """
    The context for a flow run. Data in this context is only available from within a
    flow run function.

    Attributes:
        flow: The flow instance associated with the run
        flow_run: The API metadata for the flow run
        task_runner: The task_runner instance being used for the flow run
        task_run_futures: A list of futures for task runs created within this flow run
        subflow_states: A list of states for flow runs created within this flow run
        sync_portal: A blocking portal for sync task/flow runs in an async flow
        timeout_scope: The cancellation scope for flow level timeouts
    """

    flow: Flow
    flow_run: FlowRun
    task_runner: BaseTaskRunner

    # Tracking created objects
    task_run_futures: List[PrefectFuture] = Field(default_factory=list)
    subflow_states: List[State] = Field(default_factory=list)

    # The synchronous portal is only created for async flows for creating engine calls
    # from synchronous task and subflow calls
    sync_portal: Optional[BlockingPortal] = None
    timeout_scope: Optional[CancelScope] = None

    __var__ = ContextVar("flow_run")


class TaskRunContext(RunContext):
    """
    The context for a task run. Data in this context is only available from within a
    task run function.

    Attributes:
        task: The task instance associated with the task run
        task_run: The API metadata for this task run
    """

    task: Task
    task_run: TaskRun

    __var__ = ContextVar("task_run")


class TagsContext(ContextModel):
    """
    The context for `prefect.tags` management.

    Attributes:
        current_tags: A set of current tags in the context
    """

    current_tags: Set[str] = Field(default_factory=set)

    @classmethod
    def get(cls) -> "TagsContext":
        # Return an empty `TagsContext` instead of `None` if no context exists
        return cls.__var__.get(TagsContext())

    __var__ = ContextVar("tags")


def get_run_context() -> Union[FlowRunContext, TaskRunContext]:
    """
    Get the current run context from within a task or flow function.

    Returns:
        A `FlowRunContext` or `TaskRunContext` depending on the function type.

    Raises
        RuntimeError: If called outside of a flow or task run.
    """
    task_run_ctx = TaskRunContext.get()
    if task_run_ctx:
        return task_run_ctx

    flow_run_ctx = FlowRunContext.get()
    if flow_run_ctx:
        return flow_run_ctx

    raise MissingContextError(
        "No run context available. You are not in a flow or task run context."
    )


@contextmanager
def tags(*new_tags: str) -> Set[str]:
    """
    Context manager to add tags to flow and task run calls.

    Tags are always combined with any existing tags.

    Yields:
        The current set of tags

    Examples:
        >>> from prefect import tags, task, flow
        >>> @task
        >>> def my_task():
        >>>     pass

        Run a task with tags

        >>> @flow
        >>> def my_flow():
        >>>     with tags("a", "b"):
        >>>         my_task()  # has tags: a, b

        Run a flow with tags

        >>> @flow
        >>> def my_flow():
        >>>     pass
        >>> with tags("a", b"):
        >>>     my_flow()  # has tags: a, b

        Run a task with nested tag contexts

        >>> @flow
        >>> def my_flow():
        >>>     with tags("a", "b"):
        >>>         with tags("c", "d"):
        >>>             my_task()  # has tags: a, b, c, d
        >>>         my_task()  # has tags: a, b

        Inspect the current tags

        >>> @flow
        >>> def my_flow():
        >>>     with tags("c", "d"):
        >>>         with tags("e", "f") as current_tags:
        >>>              print(current_tags)
        >>> with tags("a", b"):
        >>>     my_flow()
        {"a", "b", "c", "d", "e", "f"}
    """
    current_tags = TagsContext.get().current_tags
    new_tags = current_tags.union(new_tags)
    with TagsContext(current_tags=new_tags):
        yield new_tags
