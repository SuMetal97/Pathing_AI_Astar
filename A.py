import math

#Global variable to keep track of the final path
point_path = []
final_x = 0
final_y = 0


#Node for the path
class Node:
    def __init__(self, loc=None, x=None, y=None):
        self.x = x
        self.y = y
        self.loc = loc
        self.distance_End = 0
        self.next = []
visited = {}
BreakTheWorld = False


def main():
    #Opening and reading file locations.txt until EOF
    f = open('locations.txt', 'r')
    file = f.readlines()
    #Initializing variables
    locations = []
    Nodes = []
    ID = 0
    #Format the two txt files (not changing the file itself but how its received) so that it is easier to use
    for lines in file:
        line = lines.rstrip('\n')
        line = line.split(' ')
        loc = line[0]
        if loc == 'END':
            break
        x = line[1]
        y = line[2]
        Nodes.append(Node(loc, x, y))
        locations.append(loc)
        visited[loc] = False
        ID += 1
    #Closing file locations.txt
    f.close()
    
    #Opening and reading file connections.txt until EOF
    f = open('connections.txt', 'r')
    file = f.readlines()
    for lines in file:
        line = lines.rstrip('\n')
        line = line.split(' ')
        loc = line[0]
        if loc == 'END':
            break
        count = int(line[1])
        
        for k in range(count+1):
            for x in range(count+1):
                if (x == 0):
                    continue

                elif (x == 1):
                    continue
                #Format connections alphabetically
                elif (line[x] > line[x+1]):
                    temp = line[x]
                    line[x] = line[x+1]
                    line[x+1] = temp

        for i in range(count):
            x = locations.index(line[i + 2])
            Nodes[locations.index(loc)].next.append(Nodes[x])
    #Closing file connections.txt
    f.close()

    #Get input from user to enter in starting and final locations.
    print("Please enter in the starting location:", end = " ")
    start = input()
    #Input validation
    while start not in locations:
        print("Invalid starting location. Please try again:", end = " ")
        start = input()
    print("Please enter in the final location:", end = " ")
    end = input()
    #Input validation
    while end not in locations:
        print("Invalid final location. Please try again:", end = " ")
        end = input()
    final_x = Nodes[locations.index(end)].x
    final_y = Nodes[locations.index(end)].y

    print(final_x + " " + final_y)
    Calculate_distance(Nodes, final_x, final_y)
    for Part in Nodes:
        print(Part.loc + " " + str(Part.distance_End))
    path = [start]*len(locations)
    length = [0]*len(locations)

    #Start the path and print the path
    findPath(Nodes[locations.index(start)], path, end, length, 0, 0)
    for x in range(len(point_path)):
        print(point_path[len(point_path)-x-1])

    #Prints total length of path
    print('\n'"The total length of the path is " + str(tot_length))
    


def findPath(node,path, end, length, count, final_distance): 
    if node.loc == end:
        global BreakTheWorld
        BreakTheWorld = True
        global tot_length
        tot_length = final_distance
        return 
    if visited[node.loc]:
        return
    else:
        visited[node.loc] = True
    #create the node list and tell the code which nodes come first with respect to the estimated distance
    move = []
    for y in node.next:
        move.append(y)
    for z in range(0, len(move)-1):
        for x in range(0, len(move)-1):
            if move[x].distance_End > move[x+1].distance_End:
                tmp = move[x+1]
                move[x+1] = move[x]
                move[x] = tmp
    print("The order for " + str(node.loc) + " to check is: ")
    for order in move:
        print(order.loc)
    ######################################################################################################

    for tmp in node.next:
        #Find the right path via DFS constraints given
        final_distance += distance(node.x, node.y, tmp.x, tmp.y)
        count += 1
        findPath(tmp, path, end, length, count, final_distance)
        #If the end has been located
        if BreakTheWorld:
            point_path.append(node.loc + " to "  + tmp.loc + " length is " + str(distance(node.x, node.y, tmp.x, tmp.y)) + "    the estimated distance to the end from Node is: " + str(node.distance_End))
            break
        else:
            final_distance -= distance(node.x, node.y, tmp.x, tmp.y)

#Math function to calculate the distance between two individual nodes
def distance(x1,y1,x2,y2):
    x = math.pow(int(x1)-int(x2), 2)
    y = math.pow(int(y1)-int(y2), 2)

    return math.sqrt(x+y)

def Calculate_distance(Nodes,final_x, final_y):
    for part in Nodes:
        part.distance_End = distance(part.x, part.y, final_x, final_y)




main()