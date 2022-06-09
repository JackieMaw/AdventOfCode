# --- Day 14: Snailfish ---
https://adventofcode.com/2021/day/18

## State Representation

There are two operations we need to perform:
 1) Add two Snailfish numbers together (including reduction)
 2) Calculate the Magnitude of a Snailfish number

 How we choose to represent a Snailfish number is really quite important because that will enable the algorithm we implement.

## Algorithm

### Addition + Reduction

Addition of two Snailfish numbers is essentially just pairing two Snailfish numbers together - it's a trivial task.
The real complexity of this problem comes in Reducing the Snailfish number.

Reduction can be seen as a way of balancing or spreading the numbers out.
Any number which is 10 or greater must be split in half and consumed by it's neighbours
If the nesting gets too much, or the tree gets too deep, we need to prune the branch

# INCOMPLETE SORRY 