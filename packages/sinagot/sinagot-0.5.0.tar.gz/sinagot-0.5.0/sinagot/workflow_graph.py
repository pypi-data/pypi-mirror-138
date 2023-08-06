from typing import Type

import matplotlib.pyplot as plt
import networkx as nx

from sinagot.base import WorkflowBase


class WorkflowGraph:
    nx_graph: nx.Graph

    def __init__(self, workflow: Type[WorkflowBase]):
        self.workflow = workflow
        self._set_graph()

    def _set_graph(self) -> None:
        workflow = self.workflow
        graph = nx.DiGraph()
        graph.add_nodes_from(workflow._seeds)
        graph.add_nodes_from(workflow._steps)
        for name, step in workflow._steps.items():
            graph.add_edges_from(
                [
                    (source.name, name, {"label": step.func.__name__})
                    for source in step.args
                ]
            )
            graph.add_edges_from(
                [
                    (source.name, name, {"label": step.func.__name__})
                    for source in step.kwargs.values()
                ]
            )
        self.nx_graph = graph

    def draw(self) -> None:
        graph = self.nx_graph

        pos = nx.nx_pydot.pydot_layout(graph, prog="dot")
        edge_labels = {
            (source, dest): data["label"] for source, dest, data in graph.edges.data()
        }

        plt.figure(1, figsize=(20, 10))

        nx.draw_networkx(
            graph,
            pos=pos,
            arrows=True,
            node_color="#e1a798ff",
            font_color="#542418",
            font_weight="bold",
            node_shape="8",
            edge_color="#1a2127",
            node_size=2000,
            font_size=14,
            arrowsize=20,
        )
        nx.draw_networkx_edge_labels(
            graph,
            pos=pos,
            edge_labels=edge_labels,
            rotate=False,
            font_size=11,
            bbox={
                "boxstyle": "round",
                "ec": (1.0, 1.0, 1.0),
                "fc": (1.0, 1.0, 1.0),
                "alpha": 0.7,
            },
            alpha=0.7,
            # label_pos=0.6,
        )
