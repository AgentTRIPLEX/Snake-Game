from queue import PriorityQueue

# 0 --> NORMAL
# 1 --> CLOSED
# 2 --> OPENED
# 3 --> BARRIER
# 4 --> START
# 5 --> END
# 6 --> PATH

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.mode = 0

    def is_normal(self):
        return self.mode == 0

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.mode == 1

    def is_open(self):
        return self.mode == 2

    def is_barrier(self):
        return self.mode == 3

    def is_start(self):
        return self.mode == 4

    def is_end(self):
        return self.mode == 5

    def is_path(self):
        return self.mode == 6

    def reset(self):
        self.mode = 0

    def make_closed(self):
        self.mode = 1

    def make_open(self):
        self.mode = 2

    def make_barrier(self):
        self.mode = 3

    def make_start(self):
        self.mode = 4

    def make_end(self):
        self.mode = 5

    def make_path(self):
        self.mode = 6

def doNothing():
    pass

def algorithm(start_node, end_node, nodes, update_func=doNothing):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start_node))
    came_from = {}
    g_score = {n: float("inf") for r in nodes for n in r}
    g_score[start_node] = 0
    f_score = {n: float("inf") for r in nodes for n in r}
    f_score[start_node] = h(start_node.get_pos(), end_node.get_pos())

    open_set_hash = {start_node}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end_node:
            path = get_path(came_from, current)
            start_node.make_start()
            end_node.make_end()
            return path

        for neighbor in get_neighbors(current, nodes):
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end_node.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        update_func()

        if current != start_node:
            current.make_closed()

    return []

def get_path(came_from, current):
    path = []

    while current in came_from:
        current.make_path()
        path.append(current)
        current = came_from[current]

    return path

def reset_algorithm(nodes, closed=True, open=True, path=True):
    for row in nodes:
        for node in row:
            if closed and node.is_closed():
                node.reset()

            if open and node.is_open():
                node.reset()

            if path and node.is_path():
                node.reset()

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def get_neighbors(node, nodes):
    neighbors = []

    if (node.row < (len(nodes) - 1)) and not nodes[node.row + 1][node.col].is_barrier(): # DOWN
        neighbors.append(nodes[node.row + 1][node.col])

    if (node.row > 0) and not nodes[node.row - 1][node.col].is_barrier(): # UP
        neighbors.append(nodes[node.row - 1][node.col])

    if (node.col < (len(nodes[node.row]) - 1)) and not nodes[node.row][node.col + 1].is_barrier(): # RIGHT
        neighbors.append(nodes[node.row][node.col + 1])

    if (node.col > 0) and not nodes[node.row][node.col - 1].is_barrier(): # LEFT
        neighbors.append(nodes[node.row][node.col - 1])

    return neighbors
