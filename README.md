# Flight Connection Optimizer

## Dataset: `data/flights.csv`

Comma-separated values, one row per **directed** flight route. The sample data lists major **European** airports.

| Column | Description |
|--------|-------------|
| `origin` | Departure airport: full name plus IATA code in parentheses (e.g. `London Heathrow (LHR)`) |
| `destination` | Arrival airport, same format |
| `cost` | Ticket price in USD (non-negative number) |
| `duration_minutes` | Flight duration in minutes (non-negative number) |

The first line is the header. Fields may be quoted when they contain commas or special characters. Example:

```csv
origin,destination,cost,duration_minutes
Amsterdam Schiphol (AMS),London Heathrow (LHR),168,210
```
