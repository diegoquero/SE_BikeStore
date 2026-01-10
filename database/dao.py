from database.DB_connect import DBConnect
from model.category import Category
from model.order import Order
from model.orderItem import OrderItem
from model.product import Product


class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getCategory():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM category """
        cursor.execute(query)

        for row in cursor:
            category = Category(**row)
            result[category.id] = category


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getProducts():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM product """
        cursor.execute(query)

        for row in cursor:
            product = Product(**row)
            result[product.id] = product


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getOrder():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM `order` """
        cursor.execute(query)

        for row in cursor:
            order = Order(**row)
            result[order.id] = order


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getOrderItem():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM order_item """
        cursor.execute(query)

        for row in cursor:
            order_item = OrderItem(**row)
            result.append(order_item)


        cursor.close()
        conn.close()
        return result

