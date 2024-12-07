"""
Module: ImmunizationCampaign

This module provides the `ImmunizationCampaign` class to simulate and visualize the immunization process on a graph.
It allows for different strategies, such as random immunization, targeting high-degree nodes (hubs), or immunizing
neighbors of randomly selected nodes. The immunized nodes and their neighbors are tracked, and the graph can be 
visualized before and after immunization.

Author: Isabela Yabe
Last Modified: 02/12/2024
Status: Complete

Dependencies:
    - networkx
    - numpy
    - matplotlib.pyplot
    - random
"""


import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt

class ImmunizationCampaign:
    """
    A class to simulate an immunization campaign on a network.

    This class applies different immunization strategies to a graph, marking nodes as immunized and updating the 
    states of their neighbors. It can visualize the network before and after the immunization process.

    Attributes:
        graph (networkx.Graph): The graph representing the network.
        states (dict): A dictionary mapping nodes to their states:
            -1: Susceptible (not immunized or influenced).
             0: Neighbor of an immunized node (partially protected).
             1: Immunized.
        method (str): The immunization strategy ("random", "hubs", or "neighbors").
        immunized_nodes (list): List of nodes that have been immunized.
        neighbors_of_immunized (set): Set of nodes that are neighbors of immunized nodes.
        not_immunized (list): List of nodes that are not immunized yet.
    """
    def __init__(self, graph, method="random", seed=None):
        """
        Initializes the ImmunizationCampaign instance.

        Args:
            graph (networkx.Graph): The graph representing the network.
            method (str): The immunization strategy. Options are:
                - "random": Randomly selects nodes to immunize.
                - "hubs": Selects nodes with the highest degrees.
                - "neighbors": Selects neighbors of randomly chosen nodes.
            seed (int, optional): Seed for random number generation. Default is None.
        """
        self.graph = graph
        self.states = {node: -1 for node in graph.nodes}
        self.method = method
        self.immunized_nodes = []  
        self.neighbors_of_immunized = []
        self.not_immunized = list(self.graph.nodes())
        if seed is not None:
            random.seed(seed)

    def immunize(self, num_nodes):
        """
        Immunizes nodes in the graph based on the chosen strategy.

        Updates:
            - The `states` dictionary is updated to mark immunized nodes as `1` and their neighbors as `0` 
              (if they are not already immunized).

        Args:
            num_nodes (int): Number of nodes to immunize in this step.

        Returns:
            list: List of nodes that were immunized during this step.

        Raises:
            ValueError: If an invalid immunization strategy is provided.
        """
        
        num_not_immunized = len(self.not_immunized)

        if num_not_immunized < num_nodes:
            size = num_not_immunized
        else:
            size = num_nodes

        if self.method == "random":
            nodes_to_immunize = random.sample(self.not_immunized, size)

        elif self.method == "hubs":
            nodes_to_immunize = sorted(
                [(node, degree) for node, degree in self.graph.degree if node in self.not_immunized],
                key=lambda x: x[1], 
                reverse=True
            )[:size]
            nodes_to_immunize = [node for node, _ in nodes_to_immunize]

        elif self.method == "neighbors":
            neighbors = set()
            for node in random.sample(self.not_immunized, size):
                neighbors.update(self.graph.neighbors(node))
                if len(neighbors) >= size:
                    break
            nodes_to_immunize = list(neighbors)[:size]
        else:
            raise ValueError("Invalid immunization method.")

        for node in nodes_to_immunize:
            self.states[node] = 1 
            self.not_immunized.remove(node)

        self.immunized_nodes.extend(nodes_to_immunize)

        self.neighbors_of_immunized = set()
        for node in self.immunized_nodes:
            self.neighbors_of_immunized.update(self.graph.neighbors(node))
        self.neighbors_of_immunized -= set(self.immunized_nodes)

        for neighbor in self.neighbors_of_immunized:
            if self.states[neighbor] == -1:  
                self.states[neighbor] = 0

        return nodes_to_immunize


    def plot_graph(self, title="Graph After Immunization"):
        """
        Plots the graph with color-coded nodes based on their status and adds a legend.

        Args:
            title (str): The title of the plot. Default is "Graph After Immunization".
        """
        pos = nx.spring_layout(self.graph, seed=42)  
        node_colors = []
        for node in self.graph.nodes:
            if node in self.immunized_nodes:
                node_colors.append("green")
            elif node in self.neighbors_of_immunized:
                node_colors.append("blue")
            else:
                node_colors.append("orange")

        plt.figure(figsize=(10, 8))
        nx.draw(
            self.graph,
            pos,
            node_color=node_colors,
            with_labels=True,
            node_size=300,
            edge_color="gray",
            alpha=0.7,
        )

        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', label='Immunized Nodes', markerfacecolor='green', markersize=10),
            plt.Line2D([0], [0], marker='o', color='w', label='Neighbors of Immunized', markerfacecolor='blue', markersize=10),
            plt.Line2D([0], [0], marker='o', color='w', label='Susceptible Nodes', markerfacecolor='orange', markersize=10)
        ]
        plt.legend(handles=legend_elements, loc='upper right', title="Node Types")

        plt.title(title)
        plt.show()

if __name__ == "__main__":
    G = nx.erdos_renyi_graph(10, 0.3, seed=42)

    methods = ["random", "hubs", "neighbors"]
    campaign = ImmunizationCampaign(graph=G, method=methods[2], seed=42) 

    print("Graph before immunization:")
    campaign.plot_graph(title="Graph Before Immunization")

    immunized_nodes = campaign.immunize(num_nodes=3)
    print(f"Immunized nodes: {immunized_nodes}")
    print("States after immunization:", campaign.states)
    print("Graph after immunization:")
    campaign.plot_graph(title="Graph After Immunization")