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


    def cammino_minimo(self, nodo_sorgente):
        self._cammino_minimo=[]
        self._rifugi_visitati=set()
        self._costo_minimo=0
        lista_vicini=[]

        nodo_iniziale= self._dizionario_rifugio[nodo_sorgente.id]
        self._rifugi_visitati.add(nodo_sorgente)

        vicini=self.G.neighbors(nodo_iniziale)
        for vicino in vicini:
            lista_vicini.append(vicino)
            self.__ricorsione(vicino, lista_vicini)
        pass
    def __ricorsione(self, nodo_corrente,lista_parziale, costo_corrente, soglia):

        if nodo_corrente in self._rifugi_visitati and costo_corrente> self._costo_minimo:
            self._cammino_minimo=lista_parziale.copy()
            self._costo_minimo=costo_corrente

            return

        else:
            costo_corrente=0
            self._rifugi_visitati.add(nodo_corrente)

            if self._vincoli(lista_parziale,soglia, costo_corrente) is not None:


                for vicino in self.G.neighbors(nodo_corrente):
                    if vicino not in self._rifugi_visitati:
                        lista_parziale.append(vicino)
                        for u,v, attr in self.G.edges(vicino):
                            costo_corrente+=attr['peso']

                            self.__ricorsione(vicino,lista_parziale)

                    lista_parziale.pop()







    def _vincoli(self, lista_parziale, soglia, costo_corrente):
        if len(lista_parziale)<2:
            return
        if costo_corrente<soglia:
            return







    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
