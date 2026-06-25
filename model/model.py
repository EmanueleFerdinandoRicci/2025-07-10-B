import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._products = []
        self._idMapP = {}
        self._bestPath = []
        self._bestScore = 0

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        return DAO.getCategories()

    def getAllNodes(self):
        return self._graph.nodes

    def buildGraph(self,cat,date1,date2):
        self._graph.clear()
        self._products = DAO.getNodes(cat)
        for p in self._products:
            self._idMapP[p.product_id] = p
        self._graph.add_nodes_from(self._products)

        allEdgesDiversi = DAO.getAllEdgesDiversi(cat,date1,date2,self._idMapP)
        for e in allEdgesDiversi:
            peso = int(e.peso1) + int(e.peso2)
            self._graph.add_edge(e.p2,e.p1,weight=peso)

        allEdgesUguali = DAO.getAllEdgesUguali(cat,date1,date2,self._idMapP)
        for e in allEdgesUguali:
            peso = int(e.peso1) + int(e.peso2)
            self._graph.add_edge(e.p1,e.p2,weight=peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getEdgeGrandi(self):
        edgeGrandi = list(self._graph.edges(data=True))
        edgeGrandi.sort(key=lambda e: e[2]["weight"], reverse=True)
        return edgeGrandi

    def getNodiPiuProfittevoli(self):
        listNodesPesata = []
        for n in self._graph.nodes:
            score = 0
            for e in self._graph.out_edges(n,data=True):
                score -= e[2]["weight"]
            for e in self._graph.in_edges(n,data=True):
                score += e[2]["weight"]
            listNodesPesata.append((n,score))

        listNodesPesata.sort(key=lambda x:x[1], reverse=True)
        return listNodesPesata[0:5]

    def getBestPath(self, lun, start, end):
        self._bestPath = []
        self._bestScore = 0
        start_node = self._idMapP[int(start)]
        end_node = self._idMapP[int(end)]
        parziale = [start_node]
        self._ricorsione(parziale,lun,end)
        return self._bestPath,self._bestScore

    def _ricorsione(self,parziale,lun,end):
        if len(parziale) == lun:
            if parziale[-1] == end and self._getScore(parziale) > self._bestScore:
                self._bestPath = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)
            return

        for n in self._graph.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale,lun,end)
                parziale.pop()

    def _getScore(self,parziale):
        score = 0
        for i in range(0,len(parziale)-1):
            score += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return score