# Flight Connection Optimizer

A small command-line tool that analyzes a flight network represented as a
weighted directed graph. It answers common booking-engine questions:
cheapest route, fastest route, airports reachable within K connections,
structurally critical airports, the minimum spanning tree of the network,
and destinations reachable within a travel budget.

The sample dataset lists major **European** airports.

## How to Run

Requirements: **Python 3.8+** (uses only the standard library).

```bash
python3 main.py cheapest  "<FROM>" "<TO>"
python3 main.py fastest   "<FROM>" "<TO>"
python3 main.py reachable "<FROM>" <K>
python3 main.py critical
python3 main.py mst
python3 main.py budget    "<FROM>" <BUDGET>
```

Airport names contain spaces and parentheses, so quote them.
By default the CLI loads `data/flights.csv`.

## CSV Format: `data/flights.csv`

Comma-separated values, one row per **directed** flight route.

| Column | Description |
|--------|-------------|
| `origin` | Departure airport: full name plus IATA code in parentheses (e.g. `London Heathrow (LHR)`) |
| `destination` | Arrival airport, same format |
| `cost` | Ticket price (non-negative number) |
| `duration_minutes` | Flight duration in minutes (non-negative number) |

The first line is the header. Fields may be quoted when they contain commas
or special characters. Example:

```csv
origin,destination,cost,duration_minutes
Amsterdam Schiphol (AMS),London Heathrow (LHR),168,210
```

## Example Outputs

### cheapest

```
$ python3 main.py cheapest "London Heathrow (LHR)" "Madrid Barajas (MAD)"
Cheapest route:
  London Heathrow (LHR) -> Madrid Barajas (MAD)
  Total cost: $237.00
```

### fastest

```
$ python3 main.py fastest "Amsterdam Schiphol (AMS)" "Rome Fiumicino (FCO)"
Fastest route:
  Amsterdam Schiphol (AMS) -> Lyon-Saint-Exupery (LYS) -> Rome Fiumicino (FCO)
  Total duration: 355 minutes
```

### reachable

```
$ python3 main.py reachable "Frankfurt (FRA)" 1
Airports reachable from Frankfurt (FRA) within 1 connection(s): 21
  Amsterdam Schiphol (AMS)
  Brussels (BRU)
  ...
```

### critical

```
$ python3 main.py critical
Critical airports (articulation points):
  (none)
```

### mst

```
$ python3 main.py mst
Minimum Spanning Tree (essential routes):
  Bucharest Henri Coanda (OTP) <-> Paris Charles de Gaulle (CDG)  ($45.00)
  Edinburgh (EDI) <-> Rome Fiumicino (FCO)                        ($45.00)
  Lisbon Humberto Delgado (LIS) <-> Paris Charles de Gaulle (CDG) ($48.00)
  ...
  Total edges: 34
```

### budget

```
$ python3 main.py budget "London Heathrow (LHR)" 150
Destinations reachable from London Heathrow (LHR) within $150.00: 3
  Dublin (DUB)
  Istanbul (IST)
  London Heathrow (LHR)
```

## Complexity Analysis

`V` = number of airports, `E` = number of directed routes.

| Operation / Algorithm | Time Complexity | Space Complexity |
|-----------------------|-----------------|------------------|
| `add_edge` | O(1) average | O(1) |
| `load_csv` | O(E) | O(V + E) |
| `print_stats` | O(V) | O(1) |
| `dijkstra` (cheapest / fastest) | O((V + E) log V) | O(V) |
| `bfs_reachable` (within K hops) | O(V + E) | O(V) |
| `find_articulation_points` (brute force) | O(V * (V + E)) | O(V + E) |
| `kruskal_mst` | O(E log E) | O(V + E) |
| `budget_reachable` | O((V + E) log V) | O(V) |

### Notes

- The graph is stored as a **dictionary of adjacency lists**, so memory is
  proportional to the number of stored routes (`O(V + E)`).
- Dijkstra uses a binary **min-heap** priority queue, hence the `log V` factor.
- BFS processes each airport at most once because visits are tracked with a
  set, so the hop limit only prunes work but does not change the asymptotic
  complexity.
- The articulation-point detection here is a simplified brute-force approach:
  for each airport it rebuilds connectivity with that airport excluded. A
  Tarjan-style DFS implementation would run in `O(V + E)` but is harder to
  read.
- Kruskal uses **Union-Find with path compression**; the sorting step
  dominates the runtime.
- `budget_reachable` is Dijkstra stopped early whenever cumulative cost
  exceeds the budget, so its asymptotic cost matches Dijkstra.
