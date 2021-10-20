import math


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


class Edge:
    def __init__(self, e_id, startPoint, endPoint):
        self.e_id = int(e_id)
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.length = math.sqrt(pow((self.startPoint.x_coordinate - self.endPoint.x_coordinate), 2)
                                + pow((self.startPoint.y_coordinate - self.endPoint.y_coordinate), 2))

    def printEdge(self):
        return f"[EDGE] id: {self.e_id}, length: {self.length}\n\t\t{self.startPoint.printPoint()}\n\t\t{self.endPoint.printPoint()}"


class Route:
    # todo: szülő eltérolása, f,h,g értékek is
    def __init__(self, r_id, start, destination):
        self.r_id = r_id
        self.start = start
        self.destination = destination
        self.openNodes = set()
        self.closedNodes = set()
        self.pathNodes = set()

    def printRoute(self):
        return f"[ROUTE] id: {self.r_id}\n\t{self.start.printPoint()}\n\t{self.destination.printPoint()}"

    def heuristic(self, currentNode):
        return math.sqrt(pow((currentNode.x_coordinate - self.destination.x_coordinate), 2)
                         + pow((currentNode.y_coordinate - self.destination.y_coordinate), 2))

    def findingShortestPath(self):
        self.start.f = self.start.g = self.heuristic(self.start)
        self.openNodes.add(self.start)

        searchInProgress = True
        while searchInProgress:
            currentNode = self.findLowestF()  #find loves f node
            self.closedNodes.add(currentNode)   #put it into the closed nodes
            for neighbourNode in currentNode.neighbourNodes:
                if neighbourNode not in self.openNodes:
                    self.openNodes.add(neighbourNode)
                    neighbourNode.parent = currentNode
                    neighbourNode.h = self.heuristic(neighbourNode)
                    neighbourNode.g = self.findG(neighbourNode)
                    neighbourNode.f = neighbourNode.h + neighbourNode.g
                if neighbourNode in self.openNodes:
                    tmpG = self.findG(neighbourNode)
                    if tmpG < neighbourNode.g:
                        neighbourNode.parent = currentNode
                        neighbourNode.g = tmpG
                        neighbourNode.f = neighbourNode.g + neighbourNode.h
            if self.destination in self.closedNodes or len(self.openNodes) == 0:
                searchInProgress = False

        saveInProgress = True
        while saveInProgress:




    def findLowestF(self):
        lowestF = self.start.f
        chosenNode = self.start
        for node in self.openNodes:
            if node.f < lowestF:
                lowestF = node.f
                chosenNode = node
        return chosenNode

    def findG(self, node):
        parentNotFound = True
        while parentNotFound:
            # TODO: implement it XD


    # def findingShortestPath(self):
    #     print("\n[PATHFINDER STARTS]##################################################################################")
    #     optimalPathNotFound = True
    #     currentNode = self.start
    #     print(f"[START NODE]]: {currentNode.printPoint()}")
    #     while optimalPathNotFound:
    #         if self.heuristic(currentNode) == 0:
    #             optimalPathNotFound = False
    #         selectedEdge = self.selectNextEdge(currentNode)
    #         _currentNode = selectedEdge.endPoint if currentNode != selectedEdge.endPoint else selectedEdge.startPoint
    #         currentNode = _currentNode
    #         print(f"[CURRENT NODE]]: {currentNode.printPoint()}")
    #
    #     for edge in self.usedEdges:
    #         self.sumOfUsedEdgesLength += edge.length
    #     main.optimalLengthOrRoutes.append("{:.2f}".format(self.sumOfUsedEdgesLength))
    #
    #
    #
    # def selectNextEdge(self, currentNode):
    #     edges = currentNode.neighbourEdges
    #     if len(edges) == 0:
    #         return
    #     lowestEdgeTotalCost = None
    #     selectedEdge = None
    #     for edge in edges:
    #         endNode = edge.endPoint if edge.endPoint != currentNode else edge.startPoint
    #         currentCost = self.sumOfUsedEdgesLength + edge.length + self.heuristic(endNode)
    #         if lowestEdgeTotalCost is None or currentCost < lowestEdgeTotalCost:
    #             if edge in self.forbiddenEdges:
    #                 pass
    #             else:
    #                 if edge in self.usedEdges:
    #                     self.forbiddenEdges.add(edge)
    #                     self.usedEdges.remove(edge)
    #                 else:
    #                     self.usedEdges.add(edge)
    #                     lowestEdgeTotalCost = currentCost
    #                     selectedEdge = edge
    #
    #     # TODO: üres usedEdges-nél beszarik; Mit csináljak, ha nincs semmilyen used edge?
    #     # if selectedEdge is None:
    #     #     if self.usedEdges:
    #     #         selectedEdge = self.usedEdges.pop()
    #     #         self.forbiddenEdges.add(selectedEdge)
    #
    #     self.sumOfUsedEdgesLength += selectedEdge.length
    #     print("[CONNECTED EDGES]]: ")
    #     for item in edges:
    #         print(f"\t{item.printEdge()}")
    #     print(f"[SELECTED EDGE]:\n\t{selectedEdge.printEdge()}")
    #     return selectedEdge


class Main:
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
        self.optimalLengthOrRoutes = []

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
        print("\np: ", str(main.p))
        print("n: ", str(main.n))
        print("e: ", str(main.e))
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

    def findBestRoutes(self):
        for route in self.routes:
            route.findingShortestPath()
        self.printResults()

    def printResults(self):
        print("\n[RESULT]#############################################################################################")
        print(*self.optimalLengthOrRoutes, sep='\t')

########################################################################################################################
###########################   MM MM     A     I   NN  N   ##############################################################
###########################   M M M    AAA    I   N N N   ##############################################################
###########################   M   M   A   A   I   N  NN   ##############################################################
########################################################################################################################


main = Main()
main.readInput()  # reads and processes input
main.setClasses()  # set the Point, Edge, and Route class collections
main.pesantDebug()  # prints arrays, class collections
main.findBestRoutes()  # optimal route finding
# TODO: a végén fölös printeket/ kiíratásokat törölni, de előtte egy másolatot csinálni, GitHub save
