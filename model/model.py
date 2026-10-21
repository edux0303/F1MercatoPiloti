import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}
        # punto 2
        self._arrivo = None
        self._maxPassi = None
        self._percorsoBest = []
        self._pesoBest = -1

    # ==================== PUNTO 1 ====================

    def getAnni(self):
        return DAO.getAllYears()

    def buildGraph(self, anno1, anno2):
        self._grafo.clear()
        self._idMap = {}

        nodi = DAO.getNodi(anno1, anno2)
        self._idMap = {c.constructorId: c for c in nodi}
        self._grafo.add_nodes_from(nodi)

        for id1, id2, peso in DAO.getEdges(anno1, anno2):
            if id1 in self._idMap and id2 in self._idMap:
                self._grafo.add_edge(self._idMap[id1], self._idMap[id2], weight=peso)

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getNodiOrdinati(self):
        return sorted(self._grafo.nodes, key=lambda c: c.name)

    def getTop3(self):
        archi = []
        for u, v, dati in self._grafo.edges(data=True):
            archi.append((u, v, dati["weight"]))
        archi.sort(key=lambda x: (-x[2], str(x[0]), str(x[1])))
        return archi[:3]

    def getEsportatore(self):
        best = None
        valBest = None
        for c in self._grafo.nodes:
            val = self._grafo.out_degree(c,weight="weight") - self._grafo.in_degree(c,weight="weight")
            if valBest is None or val > valBest:
                best = c
                valBest = val

        return best, valBest

    def getNumComponentiDeboli(self):
        return nx.number_weakly_connected_components(self._grafo)

    def getCammino(self,partenza):
        self._solBest = []
        self._pesoBest = 0
        self._ricorsione([partenza],0)
        return self._solBest, self._pesoBest

    def _ricorsione(self,parziale,peso):
        if len(parziale) > len(self._solBest) or (len(parziale) == len(self._solBest) and peso > self._pesoBest):
            self._solBest = list(parziale)
            self._pesoBest = peso

        ultimo = parziale[-1]
        for v in self._grafo.successors(ultimo):
            if v.punti > ultimo.punti:
                parziale.append(v)
                self._ricorsione(parziale,peso+ self._grafo[ultimo][v]["weight"])
                parziale.pop()

    def getCostruttore(self, idC):
        return self._idMap.get(idC)
