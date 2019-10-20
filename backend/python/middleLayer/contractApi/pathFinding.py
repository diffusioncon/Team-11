from math import cos, atan, sin
import math
class pathFinder():

    xYgraph = {
    'A' : [(0, 62), ["B"]],
    'B' : [(235, 107), ["A", "C", "F", "G"]],
    'C' : [(312, 65), ["B", "D", "H"]],
    'D' : [(420, 0), ["C"]],
    'E' : [(0, 280), ["F"]],
    'F' : [(172,225), ["E","B","Q"]],
    'G' : [(355, 275), ["B", "H", "M", "Q"]],
    'H' : [(427, 235), ["C", "I", "G"]],
    'I' : [(512, 190), ["H"]],
    'J' : [(0, 355), ["K"]],
    'K' : [(193, 352), ["J", "Q", "L"]],
    'L' : [(242, 430), ["K", "M", "R"]],
    'M' : [(457, 315), ["L", "G", "N", "O"]],
    'N' : [(512, 290), ["M"]],
    'O' : [(512, 340), ["M"]],
    'P' : [(512, 385), ["R"]],
    'Q' : [(240, 330), ["K", "F", "G"]],
    'R' : [(280, 502), ["L", "P"]],
    }

    def _mapNodeToXY(self, node):
        return self.xYgraph[node][0]

    def _getDistance(self, pointA, pointB):
        a = self.xYgraph[pointA][0]
        b = self.xYgraph[pointB][0]
        x1 = abs(a[0] - b[0])
        x2 = abs(a[1] - b[1])
        return x1 + x2

    def _makeDistGraph(self):
        rett = {}
        for k, v in self.xYgraph.items():
            paths = {}
            for node in v[1]:
                paths[node] = self._getDistance(k, node)
                rett[k] = paths
        self.distGraph = rett

    def __init__(self):
        self._makeDistGraph()

    def findPath(self, initialNode, endNode):
        path = {}
        adj_node = {}
        queue = []
        for node in self.distGraph:
            path[node] = float("inf")
            adj_node[node] = None
            queue.append(node)

        path[initialNode] = 0
        while queue:
            # find min distance which wasn't marked as current
            key_min = queue[0]
            min_val = path[key_min]
            for n in range(1, len(queue)):
                if path[queue[n]] < min_val:
                    key_min = queue[n]
                    min_val = path[key_min]
            cur = key_min
            queue.remove(cur)
            #print(cur)

            for i in self.distGraph[cur]:
                alternate = self.distGraph[cur][i] + path[cur]
                if path[i] > alternate:
                    path[i] = alternate
                    adj_node[i] = cur

        ret = [endNode]
        while True:
            endNode = adj_node[endNode]
            if endNode is None:
                print("")
                break
            ret.append(endNode)
        return list(reversed([self._mapNodeToXY(r) for r in ret]))


    def xyToNode(self, x, y):
        distances=list()
        for node in self.xYgraph.items():
            x1, y1 = node[1][0]
            distances.append((sum([abs(x1-x), abs(y1-y)]), node))
        return sorted(distances, key=lambda x: x[0])[0]

    
    def XYToLatLong(self, x, y):
        cLat, cLong = 52.051532, 1.154489
        rad = 0.00001

        lat = ((x / 512) * (rad * 2)) + (cLat - rad)
        long = ((y / 512) * (rad * 2)) + (cLong - rad)
        return lat, long

    

    def convertLatLongtoNode(self, lat, long):
        cLat, cLong = 52.051532, 1.154489
        rad = 0.00001

        x = ((lat - (cLat - rad)) / (rad * 2)) * 512
        y = ((long - (cLong - rad)) / (rad * 2)) * 512
        return self.xyToNode(x,y)[1]




