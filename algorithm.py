# Implement Edmonds-Karp algorithm with step-by-step functionality

from collections import deque
import networkx as nx

class EdmondsKarp:
    """Edmonds-Karp maximum flow algorithm with step capability."""

    def __init__(self, graph: nx.DiGraph, source, sink):
        self.graph = graph
        self.source = source
        self.sink = sink
        self.flow = 0
        # create residual graph
        self.residual = nx.DiGraph()
        for u, v, data in graph.edges(data=True):
            cap = data.get("capacity", 0)
            self.residual.add_edge(u, v, capacity=cap)
            if not self.residual.has_edge(v, u):
                self.residual.add_edge(v, u, capacity=0)

    def _bfs(self):
        parent = {self.source: None}
        queue = deque([self.source])
        while queue:
            u = queue.popleft()
            for v in self.residual.successors(u):
                cap = self.residual[u][v]["capacity"]
                if cap > 0 and v not in parent:
                    parent[v] = u
                    if v == self.sink:
                        path = []
                        cur = v
                        while parent[cur] is not None:
                            prev = parent[cur]
                            path.append((prev, cur))
                            cur = prev
                        path.reverse()
                        return path
                    queue.append(v)
        return None

    def step(self):
        """Perform one augmentation step. Return details or None if done."""
        path = self._bfs()
        if not path:
            return None
        path_cap = min(self.residual[u][v]["capacity"] for u, v in path)
        for u, v in path:
            self.residual[u][v]["capacity"] -= path_cap
            self.residual[v][u]["capacity"] += path_cap
        self.flow += path_cap
        return {"path": path, "path_capacity": path_cap, "total_flow": self.flow}

    def run(self):
        """Run until no augmenting path exists."""
        steps = []
        while True:
            result = self.step()
            if result is None:
                break
            steps.append(result)
        return steps
