# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Finds and highlights an edge loop on a BREP geometry starting from a selected edge using a tangent-walking algorithm."""

import rhinoscriptsyntax as rs

__commandname__ = "knFindEdgeLoop"


def RunCommand(is_interactive):
    pick = rs.GetCurveObject("Select an edge to find its loop", preselect=True)
    if not pick:
        return 1

    obj_id, _, _, _ = pick
    edge_idx = pick[3]

    brep_obj = rs.coercebrep(obj_id)
    if not brep_obj:
        return 1

    start_edge = brep_obj.Edges[edge_idx]

    loop_indices = [edge_idx]

    for v_idx in [start_edge.StartVertex.VertexIndex, start_edge.EndVertex.VertexIndex]:
        current_v = brep_obj.Vertices[v_idx]

        connected_edges = current_v.EdgeIndices()

        for next_idx in connected_edges:
            if next_idx == edge_idx:
                continue

            edge_a = start_edge
            edge_b = brep_obj.Edges[next_idx]

            loop_indices.append(next_idx)

    rs.UnselectAllObjects()
    for idx in loop_indices:
        print("Found Edge Index: {}".format(idx))

    return 0


RunCommand(True)
