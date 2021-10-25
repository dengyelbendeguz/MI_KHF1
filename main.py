# @Author: Dengyel Bendegúz
#
# MINTA:
##############################################################################################################
# p    ....................................................azon pontpárok száma, melyek közt utat kell keresni
# n    ................................................az úthálózat kereszteződéseinek (vagy csúcsainak) száma
# e    ......................................................................az úthálózat útszakaszainak száma
# [üres sor]
# kiinduló kereszteződés id [tab] célkereszteződés id                                               ^
# kiinduló kereszteződés id [tab] célkereszteződés id                                               |
# kiinduló kereszteződés id [tab] célkereszteződés id                                               | p db sor
# kiinduló kereszteződés id [tab] célkereszteződés id                                               |
# kiinduló kereszteződés id [tab] célkereszteződés id                                               ˇ
# [üres sor]
# 0. kereszteződés x koordinátája [tab] kereszteződés y koordinátája                                ^
# 1. kereszteződés x koordinátája [tab] kereszteződés y koordinátája                                |
# 2. kereszteződés x koordinátája [tab] kereszteződés y koordinátája                                |
# 3. kereszteződés x koordinátája [tab] kereszteződés y koordinátája                                | n db sor
# 4. kereszteződés x koordinátája [tab] kereszteződés y koordinátája                                |
# ...                                                                                               |
# n. kereszteződés x koordinátája [tab] kereszteződés y koordinátája                                ˇ
# [üres sor]
# az adott útszakasz egyik kereszteződés id-je [tab] az adott útszakasz másik kereszteződés id-je   ^
# az adott útszakasz egyik kereszteződés id-je [tab] az adott útszakasz másik kereszteződés id-je   |
# az adott útszakasz egyik kereszteződés id-je [tab] az adott útszakasz másik kereszteződés id-je   | e db sor
# az adott útszakasz egyik kereszteződés id-je [tab] az adott útszakasz másik kereszteződés id-je   ˇ
##############################################################################################################
# MINTA VÉGE

import math


#  Point class, that represents a graph node
class Point:
    def __init__(self, p_id, x, y):
        self.p_id = int(p_id)
        self.x_coordinate = int(x)
        self.y_coordinate = int(y)
        self.neighbourNodes = set()
        self.neighbourEdges = set()
        self.parent = None
        self.f = 0  # total cost: g + h
        self.h = 0  # heuristic: distance from destination point
        self.g = 0  # distance between current node and start node (the sum of the paths length)

    def __eq__(self, other):
        return self.x_coordinate == other.x_coordinate and self.y_coordinate == other.y_coordinate

    def __hash__(self):
        return hash((self.x_coordinate, self.y_coordinate))

    def printPoint(self):
        return f"[NODE] id: {self.p_id}, x: {self.x_coordinate}, y: {self.y_coordinate}"

    def addNeighbourNode(self, neighbourNode):
        self.neighbourNodes.add(neighbourNode)

    def addNeighbourEdge(self, neighbourEdge):
        self.neighbourEdges.add(neighbourEdge)

    def printNeighbours(self):
        print(f"[NEIGHBOURS]\t{self.printPoint()}")
        for neighbour in self.neighbourNodes:
            print(f"\t{neighbour.printPoint()}")
        for neighbour in self.neighbourEdges:
            print(f"\t{neighbour.printEdge()}")


#  Edge class, that represents a graph edge
class Edge:
    def __init__(self, e_id, startPoint, endPoint):
        self.e_id = int(e_id)
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.length = math.sqrt(pow((self.startPoint.x_coordinate - self.endPoint.x_coordinate), 2)
                                + pow((self.startPoint.y_coordinate - self.endPoint.y_coordinate), 2))

    def printEdge(self):
        return f"[EDGE] id: {self.e_id}, length: {self.length}\n\t\t{self.startPoint.printPoint()}\n\t\t{self.endPoint.printPoint()} "


#  Route class, that represent a route in a graph
class Route:
    def __init__(self, r_id, start, destination):
        self.r_id = r_id
        self.start = start  # the starting node
        self.destination = destination  # the destination node
        self.openNodes = []
        self.closedNodes = []
        self.pathNodes = set()  # nodes that build the path
        self.optimalPathLength = 0  # length of the optimal route

    def resetNodes(self):
        for node in main.points:
            node.f = node.g = node.h = 0
            node.parent = None

    def printRoute(self):
        return f"[ROUTE] id: {self.r_id}\n\t{self.start.printPoint()}\n\t{self.destination.printPoint()}"

    #  a* algorithm to find the shortest path quick:
    def findingShortestPath(self):
        self.resetNodes()  # reset node metrics before starting the path searching

        # making the start node of the route as the current node:
        self.start.g = self.findG(self.start)
        self.start.f = self.start.g + self.heuristic(self.start)
        self.openNodes.append(self.start)

        # iterating over nodes until openNodes are empty or destination found:
        while self.destination not in self.closedNodes and len(self.openNodes) > 0:
            # setting the current node to the one with the lowest f value in the open nodes list
            currentNode = self.findLowestF()

            # switching it to the closed nodes list:
            self.closedNodes.append(currentNode)
            nodeIndex = self.openNodes.index(currentNode)
            self.openNodes.pop(nodeIndex)

            # iterating over the neighbour nodes of the current node:
            for neighbourNode in currentNode.neighbourNodes:
                # skip if it is in closed nodes:
                if neighbourNode in self.closedNodes:
                    continue

                # put it in open nodes if it is not in there (and set it's parameters)
                if neighbourNode not in self.openNodes:
                    self.openNodes.append(neighbourNode)
                    neighbourNode.parent = currentNode
                    neighbourNode.h = self.heuristic(neighbourNode)
                    neighbourNode.g = self.findG(neighbourNode)
                    neighbourNode.f = neighbourNode.h + neighbourNode.g

                # check if a better path exist to the start node via the current node (and if so, reset parameters):
                if neighbourNode in self.openNodes:
                    oldParent = neighbourNode.parent
                    neighbourNode.parent = currentNode
                    tmpG = self.findG(neighbourNode)
                    if tmpG < neighbourNode.g:
                        neighbourNode.g = tmpG
                        neighbourNode.f = neighbourNode.g + neighbourNode.h
                    else:
                        neighbourNode.parent = oldParent

        self.savePath()  # save the path after search is over

    # calculates euclidean distance from the given node to the destination of the route
    def heuristic(self, currentNode):
        return math.sqrt(pow((currentNode.x_coordinate - self.destination.x_coordinate), 2)
                         + pow((currentNode.y_coordinate - self.destination.y_coordinate), 2))

    # finds the lowest f value in the open nodes list
    def findLowestF(self):
        lowestF = self.openNodes[0].f
        chosenNode = self.openNodes[0]
        for node in self.openNodes:
            if node.f < lowestF:
                lowestF = node.f
                chosenNode = node
        return chosenNode

    # calculating the g value to the given node
    def findG(self, node):
        g = 0
        currentNode = node
        while currentNode.parent is not None:
            edge = self.findEdge(currentNode, currentNode.parent)
            g += edge.length
            currentNode = currentNode.parent
        return g

    # finding the edge that connects the 2 given nodes
    def findEdge(self, startNode, endNode):
        for edge in startNode.neighbourEdges:
            if edge.startPoint == startNode and edge.endPoint == endNode or edge.endPoint == startNode and edge.startPoint == endNode:
                return edge

    # saving the path from the start to the route and passing it to the Main class
    def savePath(self):
        if self.destination.parent is not None:
            currentNode = self.destination
            while currentNode.parent is not None:
                self.pathNodes.add(currentNode)
                currentNode = currentNode.parent
            self.optimalPathLength = self.findG(self.destination)
        main.optimalLengthOfRoutes.append("{:.2f}".format(self.optimalPathLength))


# class created to create "global" variables
class Main:
    # making the Main class singleton:
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self):
        self.p = 0
        self.n = 0
        self.e = 0
        self.p_routes = []
        self.n_coords = []
        self.e_edges = []
        self.points = []
        self.edges = []
        self.routes = []
        self.optimalLengthOfRoutes = []

    def readInput(self):
        keepReading = True
        numberOfLine = 0

        while keepReading:
            line = input()
            # initializing p, n, e
            if numberOfLine == 0:
                self.p = int(line)
                numberOfLine += 1
                continue
            if numberOfLine == 1:
                self.n = int(line)
                numberOfLine += 1
                continue
            if numberOfLine == 2:
                self.e = int(line)
                numberOfLine += 1
                continue
            if line == '':
                keepReading = False

        self.pRead()
        input()
        self.nRead()
        input()
        self.eRead()

    def pRead(self):
        tempCnt = 0
        while tempCnt < self.p:
            line = input()
            subString = line.split('\t')
            self.p_routes.append([tempCnt, subString[0], subString[1]])
            tempCnt += 1

    def nRead(self):
        tempCnt = 0
        while tempCnt < self.n:
            line = input()
            subString = line.split('\t')
            self.n_coords.append([tempCnt, subString[0], subString[1]])
            tempCnt += 1

    def eRead(self):
        tempCnt = 0
        while tempCnt < self.e:
            line = input()
            subString = line.split('\t')
            self.e_edges.append([tempCnt, subString[0], subString[1]])
            tempCnt += 1

    def setClasses(self):
        self.setPoints()
        self.setEdges()
        self.setRoutes()

    def setPoints(self):
        for item in range(len(self.n_coords)):
            p_id = self.n_coords[item][0]
            x_coord = self.n_coords[item][1]
            y_coord = self.n_coords[item][2]
            self.points.append(Point(p_id, x_coord, y_coord))

    def setEdges(self):
        for item in range(len(self.e_edges)):
            e_id = self.e_edges[item][0]
            start_p = self.points[int(self.e_edges[item][1])]
            end_p = self.points[int(self.e_edges[item][2])]
            start_p.addNeighbourNode(end_p)
            end_p.addNeighbourNode(start_p)
            edge = Edge(e_id, start_p, end_p)
            self.edges.append(edge)
            start_p.addNeighbourEdge(edge)
            end_p.addNeighbourEdge(edge)

    def setRoutes(self):
        for item in range(len(self.p_routes)):
            r_id = self.p_routes[item][0]
            start = self.points[int(self.p_routes[item][1])]
            destination = self.points[int(self.p_routes[item][2])]
            self.routes.append(Route(r_id, start, destination))

    def pesantDebug(self):
        print(f"\np: {self.p}")
        print(f"n: {self.n}")
        print(f"e: {self.e}")
        print("\np_routes:")
        print(main.p_routes)
        print("\nn_coords:")
        print(main.n_coords)
        print("\ne_edges:")
        print(main.e_edges)
        print("\n\n[NODES]")
        for item in main.points:
            item.printNeighbours()
        print("\n\n[EDGES]")
        for item in main.edges:
            print(item.printEdge())
        print("\n\n[ROUTES]")
        for item in main.routes:
            print(item.printRoute())

    # calls all routes to find their best path
    def findBestRoutes(self):
        for route in self.routes:
            route.findingShortestPath()
        self.printResults()

    # prints the output
    def printResults(self):
        print(*self.optimalLengthOfRoutes, sep='\t')
        # write to file in case to compare output to existing one:
        # with open('output.txt', 'w') as f:
        #     f.write('\t'.join(self.optimalLengthOfRoutes[1:]) + '\n')

########################################################################################################################
###########################   MM MM     A     I   NN  N   ##############################################################
###########################   M M M    AAA    I   N N N   ##############################################################
###########################   M   M   A   A   I   N  NN   ##############################################################
########################################################################################################################


main = Main()
main.readInput()  # reads and processes input
main.setClasses()  # set the Point, Edge, and Route class collections
# main.pesantDebug()  # for checking the input
main.findBestRoutes()  # optimal path finding
