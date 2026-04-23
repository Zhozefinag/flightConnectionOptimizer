import sys

from graph import FlightGraph


DATA_FILE = "data/flights.csv"


def print_usage():
    print("Usage:")
    print('  python main.py cheapest  "<FROM>" "<TO>"')
    print('  python main.py fastest   "<FROM>" "<TO>"')
    print('  python main.py reachable "<FROM>" <K>')
    print("  python main.py critical")
    print("  python main.py mst")
    print('  python main.py budget    "<FROM>" <BUDGET>')


def cmd_cheapest(graph, args):
    if len(args) != 2:
        print_usage()
        return
    origin, destination = args
    try:
        result = graph.dijkstra(origin, destination, "cost")
    except ValueError as e:
        print(f"Error: {e}")
        return
    if result is None:
        print(f"No route exists from {origin} to {destination}.")
        return
    path, total = result
    print("Cheapest route:")
    print("  " + " -> ".join(path))
    print(f"  Total cost: ${total:.2f}")


def cmd_fastest(graph, args):
    if len(args) != 2:
        print_usage()
        return
    origin, destination = args
    try:
        result = graph.dijkstra(origin, destination, "duration")
    except ValueError as e:
        print(f"Error: {e}")
        return
    if result is None:
        print(f"No route exists from {origin} to {destination}.")
        return
    path, total = result
    print("Fastest route:")
    print("  " + " -> ".join(path))
    print(f"  Total duration: {total:.0f} minutes")


def cmd_reachable(graph, args):
    if len(args) != 2:
        print_usage()
        return
    origin, k_str = args
    try:
        k = int(k_str)
    except ValueError:
        print("Error: K must be an integer.")
        return
    try:
        reachable = graph.bfs_reachable(origin, k)
    except ValueError as e:
        print(f"Error: {e}")
        return
    print(f"Airports reachable from {origin} within {k} connection(s): {len(reachable)}")
    for airport in sorted(reachable):
        print(f"  {airport}")


def cmd_critical(graph, args):
    if args:
        print_usage()
        return
    points = graph.find_articulation_points()
    print("Critical airports (articulation points):")
    if not points:
        print("  (none)")
        return
    for airport in sorted(points):
        print(f"  {airport}")


def cmd_mst(graph, args):
    if args:
        print_usage()
        return
    graph.kruskal_mst()


def cmd_budget(graph, args):
    if len(args) != 2:
        print_usage()
        return
    origin, budget_str = args
    try:
        budget = float(budget_str)
    except ValueError:
        print("Error: BUDGET must be a number.")
        return
    try:
        reachable = graph.budget_reachable(origin, budget)
    except ValueError as e:
        print(f"Error: {e}")
        return
    print(f"Destinations reachable from {origin} within ${budget:.2f}: {len(reachable)}")
    for airport in sorted(reachable):
        print(f"  {airport}")


COMMANDS = {
    "cheapest": cmd_cheapest,
    "fastest": cmd_fastest,
    "reachable": cmd_reachable,
    "critical": cmd_critical,
    "mst": cmd_mst,
    "budget": cmd_budget,
}


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    if command not in COMMANDS:
        print(f"Unknown command: {command}")
        print_usage()
        return

    graph = FlightGraph()
    graph.load_csv(DATA_FILE)
    COMMANDS[command](graph, args)


if __name__ == "__main__":
    main()
