import pymysql

# from crawler.crawler import get_crawler
#
# c = get_crawler(init=False)
# c.start()

sql = "SELECT * FROM products WHERE {} ORDER BY stock {} LIMIT {}".format("price>0 AND (stock=-1)", "", "1, 10")
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='10',
                             db='rokid',
                             charset='utf8mb4')
cursor = connection.cursor()
cursor.execute(sql)
result = cursor.fetchall()
print(result)
