import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._lista_rifugi = []
        self._getRifugio()
        self._dizionario_rifugio = {}

        for r in self._lista_rifugi:
            self._dizionario_rifugio[r.id] = r
        self.G = nx.Graph()

    """Definire le strutture dati utili"""
        # TODO

    def _getRifugio(self):
        self._lista_rifugi =DAO.readRifugio()

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        connessioni = DAO.readConnessioni(self._dizionario_rifugio,year)
        for c in connessioni:
            self.G.add_nodes_from([c.r1, c.r2])

        for c in connessioni:
            self.G.add_edge(c.r1, c.r2, peso=c.peso)


        # TODO

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        lista_pesi=[]
        for u,v, attr in self.G.edges(data=True):
                lista_pesi.append(attr['peso'])

        max_peso=max(lista_pesi)
        min_peso=min(lista_pesi)
        # TODO
        return min_peso, max_peso

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        archi_maggiori_soglia=0
        archi_minori_soglia=0
        for u,v, attr in self.G.edges(data=True):
            if attr['peso'] < soglia:
                archi_minori_soglia +=1
            else:
                if attr['peso'] > soglia:
                    archi_maggiori_soglia+=1
        return archi_minori_soglia, archi_maggiori_soglia
        # TODO

    def _cammino_minimo(self, soglia):
        a=self._cammino_minimo_ricorsione(soglia)
        b=self._cammino_minimo_nx(soglia)

        return a

    def _cammino_minimo_ricorsione(self, soglia):
        self._cammino_migliore=[]
        self._costo_minimo=100000
        for nodo in self.G.nodes:
            self.__ricorsione(nodo_corrente=nodo, lista_rifugi=[nodo], costo_corrente=0, soglia=soglia)

        return self._cammino_migliore


    def __ricorsione(self, nodo_corrente,lista_rifugi, costo_corrente, soglia):

        if costo_corrente>= self._costo_minimo:
            return

        if len(lista_rifugi)>=3 and costo_corrente < self._costo_minimo:
            self._cammino_migliore=lista_rifugi.copy()
            self._costo_minimo=costo_corrente

        for vicino in self.G.neighbors(nodo_corrente):
            if vicino not in lista_rifugi:
                peso=self.G[nodo_corrente][vicino]['peso']

                if peso >soglia:
                    lista_rifugi.append(vicino)
                    self.__ricorsione(vicino, lista_rifugi, costo_corrente+ peso, soglia)
                    lista_rifugi.pop()

    def _cammino_minimo_nx(self,soglia):

        cammino_migliore=[]
        costo_minimo=1000000

        grafo_filtrato=nx.Graph()
        for u,v, attr in self.G.edges(data=True):
            if attr['peso'] > soglia:
                grafo_filtrato.add_edge(u, v, peso=attr['peso'])

        for sorgente, cammino_minimo in nx.all_pairs_dijkstra_path(grafo_filtrato, weight='peso'):
            for target, percorso in cammino_minimo.items():
                if len(percorso)>=3:
                    costo=nx.path_weight(grafo_filtrato, percorso, weight='peso')
                    if costo< costo_minimo:
                        costo_minimo=costo
                        cammino_migliore=percorso
        return cammino_migliore

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
