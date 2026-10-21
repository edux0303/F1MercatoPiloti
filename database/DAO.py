from database.DB_connect import DBConnect
from model.Constructor import Constructor


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = "SELECT DISTINCT year FROM seasons ORDER BY year"
        cursor.execute(query)
        for row in cursor:
            results.append(row["year"])
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodi(anno1, anno2):
        """Costruttori che hanno corso nel periodo, con i punti totali."""
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT c.constructorId AS id, c.constructorRef AS ref, c.name AS nome, "
                 "c.nationality AS naz, SUM(re.points) AS punti "
                 "FROM constructors c, results re, races r "
                 "WHERE c.constructorId = re.constructorId AND re.raceId = r.raceId "
                 "AND r.year BETWEEN %s AND %s "
                 "GROUP BY c.constructorId, c.constructorRef, c.name, c.nationality")
        cursor.execute(query, (anno1, anno2))
        for row in cursor:
            c = Constructor(row["id"], row["ref"], row["nome"], row["naz"])
            c.punti = float(row["punti"])
            results.append(c)
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges(anno1, anno2):
        """(A, B, peso): piloti che hanno corso per A in un anno e per B l'anno dopo."""
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT re1.constructorId AS id1, re2.constructorId AS id2, "
                 "COUNT(DISTINCT re1.driverId) AS peso "
                 "FROM results re1, races r1, results re2, races r2 "
                 "WHERE re1.raceId = r1.raceId AND re2.raceId = r2.raceId "
                 "AND re1.driverId = re2.driverId "
                 "AND r2.year = r1.year + 1 "
                 "AND re1.constructorId <> re2.constructorId "
                 "AND r1.year BETWEEN %s AND %s AND r2.year BETWEEN %s AND %s "
                 "GROUP BY re1.constructorId, re2.constructorId")
        cursor.execute(query, (anno1, anno2, anno1, anno2))
        for row in cursor:
            results.append((row["id1"], row["id2"], row["peso"]))
        cursor.close()
        conn.close()
        return results

