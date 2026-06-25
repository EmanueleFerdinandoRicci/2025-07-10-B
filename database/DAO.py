from database.DB_connect import DBConnect
from model.category import Category
from model.edge import Edge
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getCategories():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select c.*
                    from categories c 
                    order by c.category_id"""

        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodes(cat):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select p.*
                    from products p 
                    where category_id = %s
                    order by p.product_id """

        cursor.execute(query, (cat,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdgesDiversi(cat,date1,date2,idMap):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select p1.id as p1, p2.id as p2, p1.peso as peso1, p2.peso as peso2
                    from (select p.product_id as id, sum(oi.quantity) as peso
                    from products p, order_items oi, orders o
                    where p.product_id = oi.product_id and oi.order_id = o.order_id 
                    and o.order_date between %s and %s and p.category_id = %s
                    group by p.product_id 
                    order by p.product_id) p1,
                    (select p.product_id as id, sum(oi.quantity) as peso
                    from products p, order_items oi, orders o
                    where p.product_id = oi.product_id and oi.order_id = o.order_id 
                    and o.order_date between %s and %s and p.category_id = %s
                    group by p.product_id 
                    order by p.product_id) p2
                    where p1.id != p2.id and p1.peso > p2.peso"""

        cursor.execute(query, (date1,date2,cat,date1,date2,cat,))

        for row in cursor:
            p1_obj = idMap[row["p1"]]
            p2_obj = idMap[row["p2"]]
            # Crea l'Edge passandogli gli oggetti corretti
            results.append(Edge(p1_obj, p2_obj, row["peso1"], row["peso2"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdgesUguali(cat, date1, date2, idMap):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select p1.id as p1, p2.id as p2, p1.peso as peso1, p2.peso as peso2
                   from (select p.product_id as id, sum(oi.quantity) as peso
                         from products p, \
                              order_items oi, \
                              orders o
                         where p.product_id = oi.product_id \
                           and oi.order_id = o.order_id
                           and o.order_date between %s and %s \
                           and p.category_id = %s
                         group by p.product_id
                         order by p.product_id) p1,
                        (select p.product_id as id, sum(oi.quantity) as peso
                         from products p, \
                              order_items oi, \
                              orders o
                         where p.product_id = oi.product_id \
                           and oi.order_id = o.order_id
                           and o.order_date between %s and %s \
                           and p.category_id = %s
                         group by p.product_id
                         order by p.product_id) p2
                   where p1.id != p2.id and p1.peso = p2.peso"""

        cursor.execute(query, (date1, date2, cat, date1, date2, cat,))

        for row in cursor:
            p1_obj = idMap[row["p1"]]
            p2_obj = idMap[row["p2"]]
            # Crea l'Edge passandogli gli oggetti corretti
            results.append(Edge(p1_obj, p2_obj, row["peso1"], row["peso2"]))

        cursor.close()
        conn.close()
        return results
