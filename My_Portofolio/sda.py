import mysql.connector

mydb = mysql.connector.connect(
    host="sql.freedb.tech",
    user='freedb_osama',
    password="qz!5sxM!YFyaV7V", 
    database="freedb_OsamaAbdElMohsenPortofolio", 
    auth_plugin='mysql_native_password',

)
mycursor = mydb.cursor()

print(mycursor.execute("SELECT * FROM data"))