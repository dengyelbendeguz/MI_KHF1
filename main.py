import math


class Point:
    def __init__(self, p_id, x, y):
        self.p_id = int(p_id)
        self.x_coordinate = int(x)
        self.y_coordinate = int(y)

    def printPoint(self):
        print("\t\t[NODE] id: ", str(self.p_id),", x: ", str(self.x_coordinate), ", y: ", str(self.y_coordinate))


class Edge:
    def __init__(self, e_id, startPoint, endPoint):
        self.e_id = int(e_id)
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.length = math.sqrt(pow((self.startPoint.x_coordinate - self.endPoint.x_coordinate), 2)
                                + pow((self.startPoint.y_coordinate - self.endPoint.y_coordinate), 2))

    def printEdge(self):
        print("\n\t[EDGE] id: ", self.e_id, ", length: ",self.length)
        self.startPoint.printPoint()
        self.endPoint.printPoint()


class Route:
    def __init__(self, r_id, start, destination):
        self.r_id = r_id
        self.start = start
        self.destination = destination
        self.sumOfUsedEdgesLength = 0

    def printRoute(self):
        print("\n\t[ROUTE] id: ", self.r_id)
        self.start.printPoint()
        self.destination.printPoint()

    def findingShortestPath(self):
        print("\n\n\n\n[PATHFINDER STARTS]")
        edgesOfOptimalPath = []
        optimalPathNotFound = True
        currentNode = self.start
        print("[CURRENT NODE]]:")
        print(currentNode.printPoint())
        while optimalPathNotFound:
            if self.heuristic(currentNode) == 0:
                optimalPathNotFound = False
            connectedEdges = self.findConnectedEdges(self.start)
            selectedEdge = self.selectNextEdge(connectedEdges, currentNode)
            edgesOfOptimalPath.append(selectedEdge)
            _currentNode = selectedEdge.endPoint if currentNode != selectedEdge.endPoint else selectedEdge.startPoint
            currentNode = _currentNode
            print("[CURRENT NODE]]:")
            print(currentNode.printPoint())

        sumOfEdgesInPath = 0
        for edge in edgesOfOptimalPath:
            sumOfEdgesInPath += edge.length
        main.optimalLengthOrRoutes.append("{:.2f}".format(sumOfEdgesInPath))
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX[PATH FOUND]XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

    def heuristic(self, currentNode):
        return math.sqrt(pow((currentNode.x_coordinate - self.destination.x_coordinate), 2)
                         + pow((currentNode.y_coordinate - self.destination.y_coordinate), 2))

    def findConnectedEdges(self, sourceNode):
        connectedEdges = []
        for edge in main.edges:
            if edge.startPoint == sourceNode or edge.endPoint == sourceNode:
                connectedEdges.append(edge)

        print("\t[CONNECTED EDGES]]: ")
        for item in connectedEdges:
            item.printEdge()
        return connectedEdges

    def selectNextEdge(self, edges, currentNode):
        if len(edges) == 0:
            return
        lowestEdgeTotalCost = None
        selectedEdge = None
        for edge in edges:
            endNode = edge.endPoint if edge.endPoint != currentNode else edge.startPoint
            currentCost = self.sumOfUsedEdgesLength + edge.length + self.heuristic(endNode)
            if lowestEdgeTotalCost is None or currentCost < lowestEdgeTotalCost:
                lowestEdgeTotalCost = currentCost
                selectedEdge = edge

        self.sumOfUsedEdgesLength += selectedEdge.length
        print("\t[SELECTED EDGE]: ")
        print(selectedEdge.printEdge())
        return selectedEdge


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
            self.edges.append(Edge(e_id, start_p, end_p))

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
            item.printPoint()
        print("\n\n[EDGES]")
        for item in main.edges:
            item.printEdge()
        print("\n\n[ROUTES]")
        for item in main.routes:
            item.printRoute()
        print("#######################################################################################################")

    def findBestRoutes(self):
        for route in self.routes:
            route.findingShortestPath()
        self.printResults()

    def printResults(self):
        print("#######################################################################################################")
        print("\n[RESULT]")
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
# TODO: LASSÚ!!!(és hibás)
main.findBestRoutes()  # optimal route finding
# TODO: a végén fölös printeket/ kiíratásokat törölni, de előtte egy másolatot csinálni
