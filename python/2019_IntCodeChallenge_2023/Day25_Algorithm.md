# https://adventofcode.com/2019/day/25
# --- Day 25: Cryostasis ---

## Observations

## Game Playing Logic

Explore all rooms, picking up all objects (except for dangerous ones).
Do not go through any security checkpoints until you have explored all rooms and collected all items.
Once the map is fully explored, return to the security checkpoint.
Try all combinations of items until we pass the security checkpoint.

### 1. Exporing All Rooms (Graph Discover)

To explore all rooms, make sure you try every door except for the door you came through, and last of all exit the way you came.
It doesn't really matter what order you explore the doors.
This is essentially a "depth-first" search, which is more convenient as we are physically moving through the game.
There is no benefit to a "breadth-first" search because we are not interested in the shortest path at this stage, we are just exploring the graph.

Is there a flaw in the algorithm?
What if there is a loop in the graph and you return to a previous room and then exit but along the way you missed some doors?

### 2. Navigating to the Security Checkpoint (Graph Navigation)

Once the map is completely explored, we want to get back to the security checkpoint.

Ideally we want to find the shortest path from the Hull Breach to the Security Checkpoint, so we can use a breadth-first search / Djkstra's algorithm to find the shortest path.

### 3. Passing the Security Checkpoint 

