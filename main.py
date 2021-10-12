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

class Point:
    def __init__(self, p_id, x, y):
        self.p_id = int(p_id)
        self.x_coordinate = int(x)
        self.y_coordinate = int(y)

    def printPoint(self):
        print("P id , x, y: " + str(self.p_id) + ", " + str(self.x_coordinate) + ", " + str(self.y_coordinate))

class Edge:
    def __init__(self, e_id, startPoint, endPoint):
        self.e_id = int(e_id)
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.length = math.sqrt(pow((self.startPoint.x_coordinate - self.endPoint.x_coordinate), 2)
                                + pow((self.startPoint.y_coordinate - self.endPoint.y_coordinate), 2))

    def printEdge(self):
        print("\nE id, length, P1, P2: ")
        print(self.e_id)
        print(self.length)
        self.startPoint.printPoint()
        self.endPoint.printPoint()

class Route:
    def __init__(self, r_id, start, destination):
        self.r_id = r_id
        self.start = start
        self.destination = destination

    def printRoute(self):
        print("\nR id, start, dest: ")
        print(self.r_id)
        self.start.printPoint()
        self.destination.printPoint()

    def findingShortestPath(self):
        # TODO this is the point of the whole task
        pass

class Main:
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

########################################################################################################################
########################################################################################################################
########################################################################################################################


main = Main()
main.readInput()  # reads and processes input
main.setClasses()  # set the Point, Edge, and Route class collections

# FOR TESTING INPUT, AND INPUT PROCESSING:
#
# Input:
#
# 2
# 3
# 3
#
# 0	2
# 1	2
#
# 2	0
# -4	1
# 6	3
#
# 1	0
# 1	2
# 0	2
#
# "test functions":
#
# print("\np: " + str(main.p))
# print("n: " + str(main.n))
# print("e: " + str(main.e))
# print("p_routes:")
# print(main.p_routes)
# print("n_coords:")
# print(main.n_coords)
# print("e_edges:")
# print(main.e_edges)
# for item in main.points:
#     item.printPoint()
# for item in main.edges:
#     item.printEdge()
# for item in main.routes:
#     item.printRoute()
