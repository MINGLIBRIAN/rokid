'''
Database has only one table: products

products schema
id: Scraped from web page
url: The product url
name: The product name
price: 0 price is unknown, otherwise normal value
stock: -1 stock is unknown, 0 out of stock, 101 in stock (more than 100, no specific quantity), 102 discontinued, otherwise normal value
img: The image url of the product
'''
import pymysql


class DataAccess:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='10',
                                          db='rokid',
                                          charset='utf8mb4')
        self.cursor = self.connection.cursor()

    def load_data(self, **kwargs):
        min = kwargs['min']
        max = kwargs['max']
        reverse = kwargs['order']
        unknown_price = kwargs['unknown_price']
        in_stock = kwargs['in_stock']
        out_of_stock = kwargs['out_of_stock']
        discontinued_stock = kwargs['discontinued_stock']
        unknown_stock = kwargs['unknown_stock']

        condition = self.get_price_sql(unknown_price)
        condition += self.get_stock_condition(in_stock, out_of_stock, discontinued_stock, unknown_stock)

        order = ""
        if reverse:
            order = "DESC"

        limit = "{}, {}".format(min, max - min)

        sql = "SELECT * FROM products WHERE {} ORDER BY stock {} LIMIT {}".format(condition, order, limit)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return [{'id': r[0], 'url': r[1], 'name': r[2], 'price': r[3], 'stock': r[4], 'img': r[5]} for r in result]

    def get_price_sql(self, unknown):
        if unknown:
            return ""
        return "price>0 AND "

    def get_stock_condition(self, instk, outstk, disstk, ukstk):
        sql = ["stock>0 AND stock<101"]
        if instk:
            "stock=101"
        if outstk:
            "stock=0"
        if disstk:
            "stock=102"
        if ukstk:
            "stock=-1"
        sql = "(" + " OR ".join(sql) + ")"
        return sql

    def close(self):
        self.connection.close()
