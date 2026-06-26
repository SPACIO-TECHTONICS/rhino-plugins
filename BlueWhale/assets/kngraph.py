# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs
import networkx as nx


def create_topology(curves):
    graph = nx.Graph()

    vertices = []
    for curve in curves:
        start_pt = curve.PointAtStart
        end_pt = curve.PointAtEnd
        start_vertex = (start_pt.X, start_pt.Y, start_pt.Z)
        end_vertex = (end_pt.X, end_pt.Y, end_pt.Z)
        vertices.append(start_vertex)
        vertices.append(end_vertex)

    for i, vertex_i in enumerate(vertices):
        for j, vertex_j in enumerate(vertices[i + 1 :], start=i + 1):
            if rs.Distance(vertex_i, vertex_j) < rs.UnitAbsoluteTolerance():
                graph.add_edge(vertex_i, vertex_j)

    return graph


if __name__ == "__main__":
    curves = rs.GetObjects("Select curves", rs.filter.curve)

    if curves:
        graph = create_topology(curves)
        print(
            "Graph created with {} nodes and {} edges.".format(
                graph.number_of_nodes(), graph.number_of_edges()
            )
        )
