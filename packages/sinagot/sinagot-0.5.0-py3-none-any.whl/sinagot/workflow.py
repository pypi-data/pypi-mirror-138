from __future__ import annotations
from pathlib import Path
import os
import inspect
from typing import (
    Any,
    Union,
    Dict,
)

import ray

from sinagot.base import WorkflowBase, StepBase, SeedBase
from sinagot.path_template import PathTemplate
from sinagot.workflow_graph import WorkflowGraph
from sinagot.workspace import Workspace
from sinagot.logger import get_logger


logger = get_logger()


class Workflow(WorkflowBase):
    _seeds: Dict[str, Any]
    _steps: Dict[str, Any]
    workflow_id: str
    graph: WorkflowGraph

    def __init__(self, workspace: Workspace[Workflow], workflow_id: str):
        self.workspace = workspace
        self.workflow_id = workflow_id

    def __init_subclass__(cls, **kwargs: Any):
        cls._seeds = dict(inspect.getmembers(cls, predicate=is_seed))
        cls._steps = dict(inspect.getmembers(cls, predicate=is_step))
        cls.graph = WorkflowGraph(cls)

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self.workflow_id}')"

    def _resolve_path(
        self, path: Union[str, Path, os.PathLike[Any]], **kwargs: str
    ) -> Path:
        kwargs["workflow_id"] = self.workflow_id
        path_ = os.fspath(path)
        return PathTemplate(self.workspace.root_path, path_).format(**kwargs).path

    def _run(self, step: StepBase, func: Any, **params: Any) -> ray.ObjectRef:
        logger.debug("Running %s for workflow %s", step, self.workflow_id)
        args = [self._get_node(source.name) for source in step.args]
        kwargs = {
            name: self._get_node(source.name) for name, source in step.kwargs.items()
        }
        remote_func = ray.remote(func)
        return remote_func.remote(*args, **kwargs, **params)

    def _get_node(self, name: str) -> Any:
        return type(self).__dict__[name].get_data(self)


def is_step(attribute: Any) -> bool:
    return isinstance(attribute, StepBase)


def is_seed(attribute: Any) -> bool:
    return isinstance(attribute, SeedBase)
