import networkx as nx
from database.dao import DAO
import copy

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
            #nodi
            self.G.add_nodes_from([c.r1, c.r2])

        for c in connessioni:
            #archi
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
        # return b per usare nx

    def _cammino_minimo_ricorsione(self, soglia):
        self._cammino_migliore=[]
        self._peso_minimo=100000
        # per ogni nodo, richiamo la ricorsione
        for nodo in self.G.nodes:
            self.__ricorsione(nodo_corrente=nodo, lista_rifugi=[nodo], peso_corrente=0, soglia=soglia)

        return self._cammino_migliore


    def __ricorsione(self, nodo_corrente,lista_rifugi, peso_corrente, soglia):

        if peso_corrente>= self._peso_minimo:
            return

        if len(lista_rifugi)>=3 and peso_corrente < self._peso_minimo: # vincoli
            self._cammino_migliore=copy.deepcopy(lista_rifugi)
            self._peso_minimo=peso_corrente

        for vicino in self.G.neighbors(nodo_corrente):
            if vicino not in lista_rifugi: # non torno su un nodo già visitato
                peso=self.G[nodo_corrente][vicino]['peso']

                if peso >soglia:
                    lista_rifugi.append(vicino)
                    self.__ricorsione(vicino, lista_rifugi, peso_corrente+ peso, soglia)
                    lista_rifugi.pop() # backtracking

    def _cammino_minimo_nx(self,soglia):

        cammino_migliore=[]
        peso_minimo=1000000

        # lavoro con grafi che rispettano la soglia
        grafo_filtrato=nx.Graph()
        for u,v, attr in self.G.edges(data=True):
            if attr['peso'] > soglia:
                grafo_filtrato.add_edge(u, v, peso=attr['peso'])

        for sorgente, cammino_minimo in nx.all_pairs_dijkstra_path(grafo_filtrato, weight='peso'): # per ogni nodo sorgente, calcola il cammino minimo verso tutti gli altri nodi
            for nodo_destinazione, percorso in cammino_minimo.items(): # la funzione restituisce un dizionario annidato: per ogni nodo sorgente (chiave), il valore è un dizionario
                                                                        # dove le chiavi sono i nodi di arrivo (target) e il valore è una lista di nodi (percorso)
                if len(percorso)>=3: # scarto i cammini con meno di 3 nodi
                    peso_totale=nx.path_weight(grafo_filtrato, percorso, weight='peso') # calcola il peso totale del percorso sommando il peso di tutti gli archi consecutivi
                    if peso_totale< peso_minimo:
                        peso_minimo=peso_totale # mi salvo il peso minimo
                        cammino_migliore=percorso # aggiorno il cammino migliore
        return cammino_migliore

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
