class Search:

    def __init__(self, tree):

        self.tree = tree
        self.tree_len = len(self.tree)
        self.src = self.tree_len -  2
        self.dest = self.tree_len - 1

    def run_bfs(self):

        explored_nodes = [-1 for i in range(len(self.tree))]
        explored_nodes[self.src] = self.src
        nodes_queue = [self.src]

        while len(nodes_queue) > 0:
            top_node = nodes_queue.pop(0)
            for tree_idx in range(len(self.tree)):
                if (self.tree[top_node][tree_idx][1] - self.tree[top_node][tree_idx][0]) != 0 and explored_nodes[tree_idx] == -1:
                    if tree_idx == self.dest:
                        explored_nodes[self.dest] = top_node
                        dest_path = [self.dest]
                        temp_node = self.dest
                        while temp_node != self.src:
                            temp_node = explored_nodes[temp_node]
                            dest_path.append(temp_node)
                        dest_path.reverse()
                        temp_node = 1
                        flow_total = float("inf")
                        cur_node = self.src
                        while temp_node != len(dest_path):
                            path_entry = self.tree[cur_node][dest_path[temp_node]]
                            path_diff = abs(path_entry[1]) - path_entry[0]
                            flow_total = min(flow_total, path_diff)
                            cur_node = dest_path[temp_node]
                            temp_node += 1
                        temp_node = 1
                        cur_node = self.src
                        while temp_node != len(dest_path):
                            path_entry = self.tree[cur_node][dest_path[temp_node]]
                            if path_entry[1] < 0:
                                path_entry[1] += flow_total
                            else:
                                path_entry[0] += flow_total
                            path_entry = self.tree[dest_path[temp_node]][cur_node]
                            if path_entry[1] <= 0:
                                path_entry[1] -= flow_total
                            else:
                                path_entry[0] += flow_total
                            cur_node = dest_path[temp_node]
                            temp_node += 1
                        return True
                    else:
                        explored_nodes[tree_idx] = top_node
                        nodes_queue.append(tree_idx)
        return False

def solution(entrances, exits, paths):

    max_flow = sum(map(sum, paths))
    tree = []

    # -- loop rooms in paths -- #
    for room_idx in range(len(paths)):
        tree.append([])

        # -- loop flow in rooms -- #
        for flow_idx in range(len(paths[room_idx])):

            tree[room_idx].append([0, paths[room_idx][flow_idx]])

        tree[room_idx].append([0, 0])

        # -- if room is an exit set sink to max flow-- #
        if room_idx in exits:
            tree[room_idx].append([0, max_flow])
        else:
            tree[room_idx].append([0, 0])

    # -- add 2 additional spots to tree --
    tree.append([])
    tree.append([])

    # -- loop rooms plus 2 spots -- #
    for room_idx in range(len(paths[0]) + 2):

        # -- if room is an entrance set source to max flow -- #
        if room_idx in entrances:
            tree[-2].append([0, max_flow])
        else:
            tree[-2].append([0, 0])

        # -- zero out last spot -- #
        tree[-1].append([0, 0])

    # -- init search class -- #
    search = Search(tree)

    while search.run_bfs():
        pass

    step_total = 0
    for tree_idx in range(search.tree_len):
        step_total += tree[-2][tree_idx][0]

    return step_total

entrances = [0]
exits = [3]
paths = [[0, 7, 0, 0],
         [0, 0, 6, 0],
         [0, 0, 0, 8],
         [9, 0, 0, 0]]

result = solution(entrances,exits,paths)

# --- test case 2 --- #

# entrances = [0, 1]
# exits = [4, 5]
# paths = [[0, 0, 4, 6, 0, 0],
#          [0, 0, 5, 2, 0, 0],
#          [0, 0, 0, 0, 4, 4],
#          [0, 0, 0, 0, 6, 6],
#          [0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0]]
