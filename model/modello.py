from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMapR = {}

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllShapes(self, year):
        return DAO.getAllShapes(year)

    def creaGrafo(self, year, shape):
        self._grafo.clear()
        self._idMapR.clear()

        avvistamenti = DAO.getAllNodes(year, shape)
        for a in  avvistamenti:
            self._idMapR[a.id] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
        print("2 - Nodi aggiunti")

        # Aggiungo gli archi
        for i in range(len(avvistamenti)):
            a1 = avvistamenti[i]
            for j in range(i + 1, len(avvistamenti)):
                a2 = avvistamenti[j]

                if a1.state==a2.state:
                    peso=0
                    if a1. longitude<a2.longitude:
                        peso=a2.longitude-a1.longitude
                        self._grafo.add_edge(a1, a2, weight=peso)
                    else:
                        peso=a1.longitude-a2.longitude
                        self._grafo.add_edge(a2, a1, weight=peso)

                # Controllo se esiste l'interazione
                #for inter in vicini:
                 #   if (inter.state1 == a1.id and inter.state2 == a2.id) or \
                        #    (inter.state1 == a2.id and inter.state2 == a1.id):

                        # Recupero i tempi
                       # durata1 = 0
                        #durata2 = 0

                      #  for g in avvistamenti:
                           # if g.state.upper() == a1.id and g.shape == shape:
                             #   durata1 += g.duration
                           # if g.state.upper() == a2.id and g.shape == shape:
                              #  durata2 += g.duration

                               # peso = durata1 + durata2
                              #  if peso > 0:
                                  #  self._grafo.add_edge(a1, a2, weight=peso)
        print("4 - Archi aggiunti")


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getTop5Archi(self):
        # return sorted(self._grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:10]
        archi = self._grafo.edges(data=True)
        return sorted(
            archi,
            key=lambda x: x[2]["weight"],
            reverse=True
        )[:5]

    def getCamminoMassimo(self):
        punteggio_massimo = 0
        cammino_massimo = []

        for nodo in self._grafo.nodes:
            mesi = {nodo.datetime.month: 1}

            punteggio, cammino = self.ricorsione( nodo, [nodo], mesi, 100  )

            if punteggio > punteggio_massimo:
                punteggio_massimo = punteggio
                cammino_massimo = cammino

        return punteggio_massimo, cammino_massimo

    def ricorsione(self, nodo, cammino, mesi, punteggio):
        punteggio_massimo = punteggio
        cammino_massimo = cammino.copy()

        for vicino in self._grafo.successors(nodo):
            # La durata deve essere strettamente crescente
            if vicino.duration <= nodo.duration:
                continue

            mese = vicino.datetime.month

            # Massimo 3 avvistamenti per mese
            if mesi.get(mese, 0) >= 3:
                continue

            # Punteggio del nuovo avvistamento
            nuovo_punteggio = punteggio + 100

            # Bonus se ha lo stesso mese del precedente
            if mese == nodo.datetime.month:
                nuovo_punteggio += 200

            # Aggiorno il conteggio dei mesi
            nuovi_mesi = mesi.copy()
            nuovi_mesi[mese] = nuovi_mesi.get(mese, 0) + 1

            nuovo_cammino = cammino + [vicino]

            # Continuo la ricorsione
            punteggio, cammino_trovato = self.ricorsione(
                vicino, nuovo_cammino, nuovi_mesi, nuovo_punteggio
            )

            if punteggio > punteggio_massimo:
                punteggio_massimo = punteggio
                cammino_massimo = cammino_trovato

        return punteggio_massimo, cammino_massimo