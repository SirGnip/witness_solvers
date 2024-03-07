# Custom types

Point = tuple[int, int]  # Note: This type is used to identify vertexes in the grid AND cells between the grid lines.
PointPair = frozenset[Point]
GridEdges = dict[PointPair, bool]
PointPath = list[Point]
Region = set[Point]
Regions = list[Region]
CellGrid = tuple[tuple[str, ...]]
