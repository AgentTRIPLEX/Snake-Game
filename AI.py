from directions import *
import astar
import itertools
import random

to_follow = {"data": []}

def get_nodes(grid, snake, food):
    start = None
    end = None
    g1 = []
    g2 = {}

    for x, y, w, h in grid.grid:
        r = y // h
        c = x // w
        g1.append((r, c))
        g2[(r, c)] = x, y

    g3 = []
    for row, col in sorted(g1):
        if len(g3) == row:
            g3.append([])

        g3[row].append(g2[(row, col)])

    nodes = []
    for row, cols in enumerate(g3):
        nodes.append([])
        for col, pos in enumerate(cols):
            n = astar.Node(row, col)
            nodes[row].append(n)

            if pos == snake.head_pos:
                n.make_start()
                start = n

            elif pos == food.pos:
                n.make_end()
                end = n

            elif pos in snake.get_body_pos():
                n.make_barrier()

    return nodes, start, end, g2

def get_path(grid, snake, food):
    nodes, start, end, g = get_nodes(grid, snake, food)
    path = astar.algorithm(start, end, nodes)
    path = [f.get_pos() for f in path]
    return [g[f] for f in path]

def get_move(snake, food, grid, hardcore=True):
    i = grid.grid.index(snake.head_pos + (snake.width, snake.height))

    if (i + 1) == len(grid.grid):
        i = 0
    else:
        i += 1

    x, y, w, h = grid.grid[i]
    hamiltonian_pos = x, y
    path = get_path(grid, snake, food)

    if ((snake.body_len < (len(grid.grid) // 20)) or snake.check_collision_upon_move(get_direction(snake.head_pos, hamiltonian_pos))) and (len(path) > 0):
        if len(path) > 0:
            direction = get_direction(snake.head_pos, path[-1])
        else:
            for direction in {NORTH:[NORTH, EAST, WEST], SOUTH: [SOUTH, EAST, WEST], EAST: [EAST, NORTH, SOUTH], WEST: [WEST, NORTH, SOUTH]}[snake.direction]:
                if not snake.check_collision_upon_move(direction):
                    break

    else:
        direction = get_direction(snake.head_pos, hamiltonian_pos)

    return direction

def get_direction(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2

    if x1 > x2:
        return WEST

    elif x1 < x2:
        return EAST

    elif y1 > y2:
        return NORTH

    elif y1 < y2:
        return SOUTH
