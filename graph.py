import csv


# FlightGraph: weighted directed graph using a dictionary of adjacency lists.
# Each key is an airport. Each value is a list of (destination, cost, duration) tuples.
#
# Time complexity:
#   add_edge       -> O(1) average
#   load_csv       -> O(E) where E is number of routes in the CSV
#   print_stats    -> O(V) where V is number of airports
# Space complexity: O(V + E)
class FlightGraph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, origin, destination, cost, duration):
        if origin not in self.adj:
            self.adj[origin] = []
        if destination not in self.adj:
            self.adj[destination] = []
        self.adj[origin].append((destination, float(cost), float(duration)))

    def load_csv(self, filepath):
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.add_edge(
                    row["origin"],
                    row["destination"],
                    row["cost"],
                    row["duration_minutes"],
                )

    def print_stats(self):
        airports = len(self.adj)
        routes = sum(len(edges) for edges in self.adj.values())
        print(f"Airports: {airports}")
        print(f"Routes: {routes}")
