# --- Day 19: Beacon Scanner ---
https://adventofcode.com/2021/day/19

## Problem Summary

Each scanner can be seen as a cube of space containing a number of beacons. These cubes actually overlap each other and we need to figure out where the cubes fit, much like building a puzzle. In order to find the right place for each cube we need to rotate each cube and try to fit it to the other cubes.

A. Build the Puzzle Space

1. Rotate
2. Fit

B. Answer the Questions

1. How many beacons are there?
2. What is the largest Manhattan distance between any two scanners?

## A. Build the Puzzle Space

Imagine that we have a pile of cubes (these are our puzzle pieces) and an empty space where we are building our puzzle.

1. Take the first cube and use it as the center of our puzzle space.
2. Take the next cube from the pile and try to FIT it somewhere in the puzzle space. If it doesn't FIT, try to ROTATE it (up to 23 times) to see if it will FIT.
3. If it does FIT, add it to our puzzle space. Also, make a note of where you put it because you'll need this information for Part Two.
4. If it doesn't FIT anywhere, put it aside to try again later.
5. If you still have more cubes left to try, go back to step 2.

Note: because we know that the puzzle has no gaps - no missing pieces, we know that on each round we will find at least cube (puzzle piece) which should fit our puzzle space.

In the best case, if we are very lucky, every piece we pickup will fit somewhere, making 36 fitting attempts.
In the worst case, if we are very unlucky, we will have to try all the remaining pieces before we find something that fits, making 666 fitting attempts. 36 + 35 + 34 + ... + 1 = (37/2)*36 = 666

For each fitting attempt, we might have to try 24 rotations.

### Rotate

For 2 dimensions, there are 4 possible rotations, which can be achieved by taking the original space and rotating 90' 3 times.
To rotate by 90': (x, y) => (y, -x)

For 3 dimensions, there are 24 possible rotations, which is best understood by looking at a 6-sided cube:
- As the cube has 6 faces, it cube can be facing 6 directions. Imagine: north, south, east, west, up, down.
- And for each of those 6 directions, you could spin the cube around in 4 possible 2-dimensional rotations leaving the 3rd dimension fixed.
- 6 x 4 = 24 QED

### Fit

Well how would know if this cube actually fits?

At least 12 of the beacons in the cube should be exactly the same distance away from beacons in the puzzle space.
So we calculate the distance from every cube beacon to every space beacon, and if we get 12 distances which are the same, then we have found a successful fit.
We can add this cube to the puzzle space with the distance we have calculated as our offset.

offset = (-dx, -dy, -dz)

We could optimize this further by reducing the search space...

## B. Answer the Questions

## Part One - How many beacons are there?

Since our puzzle space only counts each beacon once, to answer this question we just have to count the number of beacons in our space.

## Part Two - What is the largest Manhattan distance between any two scanners?

In Part One we found the relative location of all the scanners, so now all we have to do is calculate the "Manhattan Distance" between all the pairs of scanners and find the Max. This step is trivial to code and although the performance is n2 it's not really a problem for us because the number of scanners is relatively small. Since we have 37 scanners, the number of pairs we have is 37 x 36 = 1332, so we only need to do 1332 simple calculations.