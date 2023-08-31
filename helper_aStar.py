import csv
import numpy as np
class Node: # define a Node class
    def __init__(self, parent, cost, position):
        self.parent = parent
        self.cost = cost
        self.position = position
def remove_node_frontier(node, frontier):
    pos = node.position
    new_frontier = []
    for item in frontier:
        if item.position != pos:
            new_frontier.append(item)
    return new_frontier
def compute_node_cost(pos, goal):
    x, y = pos
    x_goal, y_goal = goal
    cost = np.sqrt((x_goal-x)**2 + (y_goal-y)**2)
    return cost
def is_in_map(pos, grid_dim):
    (max_x, max_y) = grid_dim # unroll the dimensions
    (x, y) = pos # unroll the position coordinates
    x_in = (x <= max_x) & (x >= 0) # logical x in map
    y_in = (y <= max_y) & (y >= 0) # logical y in map
    return bool(x_in*y_in) # only true if both true
def compute_successors(current_node, grid, seen):
    movements = [(1,0), (-1,0), (0,1), (0,-1)]
    x_0, y_0 = current_node.position
    grid_dim = (len(grid)-1, len(grid[0])-1)       
    successors = []
    for movement in movements:
        dx, dy = (movement[0], movement[1])
        next_pos = (x_0+dx, y_0+dy)
        cond1 = is_in_map(next_pos, grid_dim) # if its on the map
        if cond1:
            cond2 = grid[next_pos[0], next_pos[1]] != 0 # if not wall
            cond3 = next_pos not in [item.position for item in seen] # dont go to any already seen
            if bool(cond2*cond3):
                cost = compute_node_cost(next_pos, grid_dim)
                new_node = Node(current_node, cost, next_pos)
                successors.append(new_node)
    return successors
def pick_node_from_list(node_list):
    if len(node_list) == 1:
        current_node = node_list[0]
        return current_node
    current_node = Node(None, np.inf, (0,0)) # initialize current node
    for node in node_list:
        if node.cost < current_node.cost: # pick up the node with least cost
            current_node = node
    return current_node
def generate_step(grid, frontier, seen, current_node):
    seen.append(current_node)
    frontier = remove_node_frontier(current_node, frontier)
    successors = compute_successors(current_node, grid, seen)
    for son in successors:
        frontier.append(son)
    current_node = pick_node_from_list(successors)
    x, y = current_node.position
    grid[x, y] = 4 # paint blue  
    return grid, frontier, seen, current_node