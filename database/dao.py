from database.DB_connect import DBConnect
from model.rifugio import Rifugio
from model.connesione import Connessione

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """

    @staticmethod
    def readRifugio():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "select * from rifugio"
        cursor.execute(query)
        for row in cursor:
            result.append(Rifugio(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def readConnessioni(dizionario_rifugio, year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select id_rifugio1 as o1, id_rifugio2 as o2, anno, distanza, difficolta
                        from connessione c
                        where c.id_rifugio1< c.id_rifugio2 AND 
                        c.anno<=%s 
                        group by id_rifugio1, id_rifugio2"""
        cursor.execute(query, (year,))


        for row in cursor:
            o1 = dizionario_rifugio[row['o1']]
            o2 = dizionario_rifugio[row['o2']]
            distanza=float(row['distanza'])
            difficolta=(row['difficolta'])

            if difficolta=='facile':
                fattore_difficolta=1.0
            elif difficolta=='media':
                fattore_difficolta = 1.5
            else:
                if difficolta=='difficile':
                    fattore_difficolta=2.0

            peso=distanza*fattore_difficolta

            result.append(Connessione(o1, o2, distanza, difficolta,peso))
        cursor.close()
        conn.close()
        return result
