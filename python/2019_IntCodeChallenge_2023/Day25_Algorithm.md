# https://adventofcode.com/2019/day/25
# --- Day 25: Cryostasis ---

## Observations

## Game Playing Logic

Explore all rooms, picking up all objects (except for dangerous ones).
Do not go through any security checkpoints until you have explored all rooms and collected all items.
Once the map is fully explored, return to the security checkpoint.

### Exporing All Rooms

To explore all rooms, make sure you try every door except for the door you came through, and last of all exit the way you came.
This is essentially a "depth-first" search, which is more convenient as we are physically moving through the game.
There is no benefit to a "breadth-first" search because we are not interested in the shortest path at this stage, we are just exploring the graph.

### Navigating to the Security Checkpoint

