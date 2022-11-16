import pymysql
pymysql.install_as_MySQLdb()

db = pymysql.connect(host="localhost", user="root", password="admin", database="askme_data")

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()

db.close()
