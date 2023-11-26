# PathFindingAlgorithmVisualiser

***
Program utilising grids to visualise how the A* and Dijkstra algorithm find the shortest path between a start node and an end node with barriers in between them.
- Orange square represents the start node.
- Turquoise square represents the end node.
- Black square represents a barrier.
- Green sqaure represents that this node has not been completely explored.
- Red square represents that this node has been completely explored.
- Purple square represents a node in the shortest path found from start to end.

## How to use the program

***
When the code is ran it will open a window filled with grids. 
- Left click to put the start node and then the end node.
- Additional left clicks will create brarriers.
- Right click to erase a node.
- After setting up the start node, end nodes and barriers, press A on keyboard for the A* algorithm visualisation or press SPACE for Dijkstra.
- Press R to reset the bord to remove the red, green and purple nodes.
- Press C to clear the board.

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

## Sources
The packages used by this application are specified in `requirements.txt`
