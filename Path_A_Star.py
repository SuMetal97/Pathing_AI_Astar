import heapq as heap
from math import sqrt
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

class PQ():
    def __init__(self):
        self.queue = []
        self.map = {}
        self.delete = 'deleted'

    def push(self, task, pri=0):
        if task in self.map:
            self.remove(task)
        entry = [pri, task]
        self.map[task] = entry
        heap.heappush(self.queue, entry)

    def remove(self, task):
        entry = self.map.pop(task)
        entry[-1] = self.delete

    def pop(self):
        while self.queue:
            pri, task = heap.heappop(self.queue)
            if task is not self.delete:
                del self.map[task]
                return (pri, task)


class Map():

    def __init__(self, con_file, loc_file):
        self.locate = {}
        self.connect = {}
        # Maps a node to its location
        loc = open(loc_file, 'r')
        for x in loc:
            line = x.rstrip('\n')  # rstrip
            formatted_line = line.split()
            self.locate[formatted_line[0]] = formatted_line[1:]
        del self.locate["END"]
        # Maps a node to its connection
        con = open(con_file, 'r')
        for x in con:
            line = x.rstrip('\n')  # rstrip
            formatted_line = line.split()
            self.connect[formatted_line[0]] = formatted_line[2:]
        del self.connect["END"]
        # close files
        loc.close()
        con.close()

    def excludes(self, node):
        if node not in self.connect.keys():
            print(node + "doesn't exist")
            return -1
        exclude = self.connect[node]
        del self.connect[node]
        del self.locate[node]

        for x in exclude:
            lists = self.connect[x]
            lists.remove(node)

    def calc_heur(self, node, end, heur):
        if heur == 1:
            return 1
        else:
            return self.calc(node, end)

    def make_Graph(self):
        for node in self.locate.keys():
            G.add_node(str(node),pos = (node[0], node[1]) )
        for node  in self.connect.keys():
            loc = self.connect[node]

            for neighbors in loc:

                G.add_edge(str(node), str(neighbors), weight = self.calc(node,neighbors))


    def calc(self, a, b):
        loc1 = self.locate[a]
        x1 = int(loc1[0])
        y1 = int(loc1[1])
        loc2 = self.locate[b]
        x2 = int(loc2[0])
        y2 = int(loc2[1])
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def print_Path(self, final_path, heur):
        if final_path == []:
            print("No Path")
        else:
            final_path.reverse()
            total = 0

            for x in range(0, len(final_path) - 1):
                if heur == 0:
                    dist = self.calc(final_path[x], final_path[x + 1])

                    total += dist
                    print(final_path[x] + " to " + final_path[x + 1] + " length %.1f" % dist)
                else:
                    total += 1
                    print(final_path[x] + " to " + final_path[x + 1] + "length 1")
            print("Total path length = %.1f" % total)

    def make_Path(self, prev, current):
        path = [current]
        while current in prev.keys():
            current = prev[current]
            path.append(current)
        return path

    def as_algorithm(self, start, end, heur, step):
        # Set initial values and variables
        prev_map = {}
        open_nodes = PQ()
        closed_nodes = []
        cost = {}
        cost[start] = 0
        total_cost = {}
        cost_estimate = self.calc_heur(start, end, heur)
        # Pushes start node onto queue
        open_nodes.push(start, cost_estimate)
        total_cost[start] = cost_estimate

        # Open nodes aren't empty
        while open_nodes.map:
            current = open_nodes.pop()
            current_node = current[1]

            if step:
                print("\nSelected city: " + current_node)

            if current_node == end:
                return self.make_Path(prev_map, current_node)

            closed_nodes.append(current_node)
            neighbors = self.connect[current_node]
            if step:
                print("Possible cities: %s" % neighbors)

            for neighbor in neighbors:
                if neighbor in closed_nodes:
                    continue
                # Calculate cost to neighbor
                if heur:
                    cost_neighbor = 1 + cost[current_node]
                else:
                    cost_neighbor = self.calc(current_node, neighbor) + cost[current_node]

                # Calculate heuristic cost estimate from neighbor to end
                cost_estimate = self.calc_heur(neighbor, end, heur)
                total_cost_neighbor = cost_estimate + cost_neighbor
                # Checks to see if there is a better path
                if neighbor in open_nodes.map.keys():
                    if total_cost_neighbor >= total_cost[neighbor]:
                        continue
                # Else add neighbor to queue and update values
                cost[neighbor] = cost_neighbor
                open_nodes.push(neighbor, total_cost_neighbor)
                total_cost[neighbor] = total_cost_neighbor
                prev_map[neighbor] = current_node

            if step:
                print("Cities at end of possible paths:", end=" ")
                for x in open_nodes.queue:
                    if x[1] != "deleted":
                        print(x[1] + "(%.1f)," % x[0], end=' ')
                print("\n")
                print("****************************************************************************************")

        # No path existed
        return []




def main():
    # Initalize a map
    map = Map("connections.txt", "locations.txt")

    # User input for starting node and input validation
    while 1:
        print("Please enter in the starting location:", end=" ")
        begin = str(input())
        if begin not in map.connect.keys():
            print("Incorrect selection, please try again.\n")
        else:
            break
    # User input for end node and input validation
    while 1:
        print("\nPlease enter in the final location:", end=" ")
        end = str(input())
        if end not in map.connect.keys():
            print("Incorrect selection, please try again.")
        else:
            break
    map.make_Graph()
    # Allows user to exclude 1 or more cities
    print("\nWould you like to exclude any cities (yes or no)?", end=" ")
    answer = str(input())
    if answer == "yes":
        print("\nPlease enter in the nodes you wish to bypass seperated by a space:", end=" ")
        excluding = (input())
        # Input validation
        if excluding not in map.connect.keys():
            print("Incorrect selection, please try again:", end=" ")
            excluding = (input())
            exclude = excluding.split()
        else:
            exclude = excluding.split()
        for x in exclude:
            map.excludes(x)
    else:
        answer = "no"

    print("\nStraight line distance (0) or fewest cities (1)?:", end=" ")
    heur = int(input())
    while heur != 1 and heur != 0:
        print("Error try again (0 or 1):", end=" ")
        heur = int(input())

    print("\nWould you like to see a step by step solution (yes or no)?:", end=" ")
    step = str(input())
    while step != "yes" and step != "no":
        print("Error try again (yes or no):", end=" ")
        step = str(input())
    if step == "yes":
        step = True
    else:
        step = False

    # Prints final path
    final_path = map.as_algorithm(begin, end, heur, step)
    print("----------------------------------------------------------------------------------------")
    print("----------------------------------------------------------------------------------------")
    print("The final solution path is:")
    map.print_Path(final_path, heur)
    pos = nx.spring_layout(G)  # positions for all nodes


    node_colors = ["green" if n in final_path else "gold" for n in G.nodes()]

    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='b', width=1,
            alpha=0.7)  # with_labels=true is to show the node number in the output graph

    # labels

    plt.axis('on')
    plt.show()

main()
