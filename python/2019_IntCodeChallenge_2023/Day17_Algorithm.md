# https://adventofcode.com/2019/day/17
# --- Day 17: Set and Forget ---

## Part A - Convert Output to ASCII

When you run the IntCode program for Day17, it will output a 2-d view of a scaffold.
You need to collect the output, convert the int to ascii characters, which will produce something like this:

..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..

You need to locate all the intersection points, and calculate the sum of the alignment parameters (X * Y).

### How do I know if something is an intersection?

For each intersection point, there should be a piece of scaffold in all 4 points above, below, right and left.

.A.
L#R
.B.

## Part B - Give the Robot Instructions for traversing the Scaffold

There are two parts to this problem:
1> Find instructions to traverse the scaffold

R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2

2> Reduce to common functions / compression / factoring

Main routine: A,B,C,B,A,C
Function A:   R,8,R,8
Function B:   R,4,R,4,R,8
Function C:   L,6,L,2

Then you execute your IntCode program again, this time "waking the robot up" and you are able to INPUT your functions into the running program which will move the robot through the grid.

### Option 1 - Manual Hack

You can manually traverse the scaffold writing down the instructions. This is when you will discover that traversing the scaffold is simpler than you think - you just keep going until you cannot go anymore, then you find another direction and start going that way, until you cannot go anymore.

Once you have the traversal instructions, you can then manually inspect the instructions looking for commonality.

### Option 2 - Too Lazy? Use your brain!

1> Find instructions to traverse the scaffold

The robot should keep track of it's location and which direction it's facing.
The robot should attempt to move 1 step forward until it cannot, then it should attempt a different direction.

2> Reduce to common functions

R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2
==>
Main routine: A,B,C,B,A,C
Function A:   R,8,R,8
Function B:   R,4,R,4,R,8
Function C:   L,6,L,2

Find the longest possible substring which starts at the beginning of the instructions and is repeated. (great interview question)
This will be your first function. Remove all occurances of this substring and try again.

R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2 => R,8,R,8
_______,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,_______,L,6,L,2

_______,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,_______,L,6,L,2 => R,4,R,4,R,8
_______,___________,L,6,L,2,___________,_______,L,6,L,2

_______,___________,L,6,L,2,___________,_______,L,6,L,2 => L,6,L,2
_______,___________,_______,___________,_______,_______